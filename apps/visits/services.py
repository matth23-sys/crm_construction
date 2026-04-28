# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.notifications.services import send_visit_reminder

from .models import (
    ReminderDeliveryStatus,
    ReminderType,
    TechnicalVisit,
    VisitReminderLog,
    VisitStatus,
)


def create_technical_visit(actor, **validated_data):
    validated_data["created_by"] = actor
    validated_data["updated_by"] = actor

    visit = TechnicalVisit(**validated_data)
    visit.full_clean()
    visit.save()

    return visit


def update_technical_visit(visit, actor, **validated_data):
    validated_data["updated_by"] = actor

    for attr, value in validated_data.items():
        setattr(visit, attr, value)

    visit.full_clean()
    visit.save()

    return visit


def reschedule_technical_visit(visit, new_scheduled_for, actor, reason=""):
    visit.scheduled_for = new_scheduled_for
    visit.status = VisitStatus.RESCHEDULED
    visit.updated_by = actor

    visit.full_clean()
    visit.save()

    return visit


def _get_visit_local_datetime(visit):
    scheduled_for = getattr(visit, "scheduled_for", None)

    if not scheduled_for:
        return None

    try:
        return timezone.localtime(scheduled_for)
    except Exception:
        return scheduled_for


def _get_visit_local_date(visit):
    visit_datetime = _get_visit_local_datetime(visit)

    if not visit_datetime:
        return None

    return visit_datetime.date()


def _already_sent_successfully(visit, reminder_type, execution_date):
    return VisitReminderLog.objects.filter(
        visit=visit,
        reminder_type=reminder_type,
        execution_date=execution_date,
        status=ReminderDeliveryStatus.SENT,
    ).exists()


def _is_due_for_main_reminder(visit, run_date):
    visit_date = _get_visit_local_date(visit)

    if not visit_date:
        return False, None

    if (
        visit.reminder_type == ReminderType.DAY_BEFORE
        and visit_date == run_date + timedelta(days=1)
    ):
        return True, ReminderType.DAY_BEFORE

    if (
        visit.reminder_type == ReminderType.SAME_DAY
        and visit_date == run_date
    ):
        return True, ReminderType.SAME_DAY

    return False, None


def _is_due_for_two_hours_before(visit, run_datetime, lookahead_minutes=15):
    """
    Recordatorio automático 2 horas antes.

    Funciona mejor si el cron se ejecuta cada 15 minutos.
    Ejemplo:
    - Visita: 10:00
    - Recordatorio objetivo: 08:00
    - Si el cron corre entre 08:00 y 08:14, se envía.
    """
    visit_datetime = _get_visit_local_datetime(visit)

    if not visit_datetime:
        return False

    reminder_datetime = visit_datetime - timedelta(hours=2)
    window_start = run_datetime
    window_end = run_datetime + timedelta(minutes=lookahead_minutes)

    return window_start <= reminder_datetime < window_end


def _send_if_not_duplicated(
    *,
    visit,
    reminder_type,
    execution_date,
    retry_failed=False,
):
    if _already_sent_successfully(
        visit=visit,
        reminder_type=reminder_type,
        execution_date=execution_date,
    ) and not retry_failed:
        return "skipped"

    try:
        with transaction.atomic():
            success, log = send_visit_reminder(
                visit,
                reminder_type,
                execution_date=execution_date,
                force_retry=retry_failed,
            )

        if success:
            return "sent"

        if log and log.status == ReminderDeliveryStatus.FAILED:
            return "failed"

        return "skipped"

    except IntegrityError:
        return "skipped"


def process_due_visit_reminders(run_date=None, retry_failed=False):
    """
    Procesa recordatorios pendientes para visitas técnicas.

    Incluye:
    - DAY_BEFORE: según opción escogida en la visita.
    - SAME_DAY: según opción escogida en la visita.
    - TWO_HOURS_BEFORE: automático para toda visita con reminder_enabled=True.
    """
    run_datetime = timezone.localtime()

    if run_date is None:
        run_date = run_datetime.date()

    sent_count = 0
    failed_count = 0
    skipped_count = 0

    visits = (
        TechnicalVisit.objects
        .filter(
            reminder_enabled=True,
            status=VisitStatus.SCHEDULED,
        )
        .select_related(
            "client",
            "project",
            "responsible",
        )
        .order_by("scheduled_for")
    )

    for visit in visits:
        due_main, main_reminder_type = _is_due_for_main_reminder(
            visit=visit,
            run_date=run_date,
        )

        if due_main:
            result = _send_if_not_duplicated(
                visit=visit,
                reminder_type=main_reminder_type,
                execution_date=run_date,
                retry_failed=retry_failed,
            )

            if result == "sent":
                sent_count += 1
            elif result == "failed":
                failed_count += 1
            else:
                skipped_count += 1

        if _is_due_for_two_hours_before(
            visit=visit,
            run_datetime=run_datetime,
            lookahead_minutes=15,
        ):
            result = _send_if_not_duplicated(
                visit=visit,
                reminder_type=ReminderType.TWO_HOURS_BEFORE,
                execution_date=run_date,
                retry_failed=retry_failed,
            )

            if result == "sent":
                sent_count += 1
            elif result == "failed":
                failed_count += 1
            else:
                skipped_count += 1

    return {
        "processed_date": run_date,
        "sent": sent_count,
        "failed": failed_count,
        "skipped": skipped_count,
    }