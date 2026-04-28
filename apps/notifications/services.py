# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils import timezone

from apps.visits.models import (
    ReminderDeliveryStatus,
    ReminderType,
    VisitReminderLog,
)

logger = logging.getLogger(__name__)


def _model_has_field(model, field_name):
    """
    Verifica si el modelo tiene un campo específico.
    Esto permite soportar execution_date si ya existe en VisitReminderLog,
    sin romper proyectos donde aún no fue agregado.
    """
    return any(field.name == field_name for field in model._meta.get_fields())


def _build_visit_detail_url(visit):
    """
    Construye URL absoluta hacia el detalle de la visita.
    Usa SITE_URL si está configurado.
    """
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")

    try:
        detail_path = reverse("visits:detail", kwargs={"pk": visit.pk})
    except NoReverseMatch:
        detail_path = ""

    if site_url and detail_path:
        return f"{site_url}{detail_path}"

    return detail_path or site_url


def _get_visit_datetime_display(visit):
    """
    Devuelve una fecha/hora legible para plantillas.
    """
    scheduled_for = getattr(visit, "scheduled_for", None)

    if not scheduled_for:
        return ""

    try:
        return timezone.localtime(scheduled_for).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return scheduled_for.strftime("%d/%m/%Y %H:%M")


def _get_existing_success_log(visit, reminder_type, execution_date):
    """
    Revisa si ya existe un envío exitoso para evitar duplicados.

    Si el modelo tiene execution_date, lo usa.
    Si no lo tiene, usa created_at__date como fallback.
    """
    filters = {
        "visit": visit,
        "reminder_type": reminder_type,
        "status": ReminderDeliveryStatus.SENT,
    }

    if _model_has_field(VisitReminderLog, "execution_date"):
        filters["execution_date"] = execution_date
    else:
        filters["created_at__date"] = execution_date

    return VisitReminderLog.objects.filter(**filters).first()


def _create_reminder_log(
    *,
    visit,
    reminder_type,
    status,
    recipient_email,
    execution_date,
    sent_at=None,
    error_message="",
):
    """
    Crea un log de recordatorio respetando campos opcionales del modelo.
    """
    data = {
        "visit": visit,
        "reminder_type": reminder_type,
        "status": status,
        "recipient_email": recipient_email or "",
        "error_message": error_message or "",
    }

    if sent_at is not None:
        data["sent_at"] = sent_at

    if _model_has_field(VisitReminderLog, "execution_date"):
        data["execution_date"] = execution_date

    return VisitReminderLog.objects.create(**data)


def send_visit_reminder(
    visit,
    reminder_type,
    *,
    execution_date=None,
    force_retry=False,
):
    """
    Envía un correo de recordatorio para una visita técnica.

    Retorna:
    - (True, log) si el correo fue enviado correctamente.
    - (False, log) si falló o si ya existía un envío exitoso.
    - (False, existing_log) si se omitió por anti-duplicado.
    """
    if execution_date is None:
        execution_date = timezone.localdate()

    existing_success_log = _get_existing_success_log(
        visit=visit,
        reminder_type=reminder_type,
        execution_date=execution_date,
    )

    if existing_success_log and not force_retry:
        return False, existing_success_log

    responsible = getattr(visit, "responsible", None)
    recipient = (getattr(responsible, "email", "") or "").strip()

    if not recipient:
        log = _create_reminder_log(
            visit=visit,
            reminder_type=reminder_type,
            status=ReminderDeliveryStatus.FAILED,
            recipient_email="",
            execution_date=execution_date,
            error_message="El responsable no tiene dirección de correo electrónico.",
        )
        return False, log

    visit_detail_url = _build_visit_detail_url(visit)

    context = {
        "visit": visit,
        "reminder_type": reminder_type,
        "client": getattr(visit, "client", None),
        "responsible": responsible,
        "scheduled_for": getattr(visit, "scheduled_for", None),
        "visit_datetime": _get_visit_datetime_display(visit),
        "location": getattr(visit, "location", ""),
        "project": getattr(visit, "project", None),
        "site_url": getattr(settings, "SITE_URL", ""),
        "visit_detail_url": visit_detail_url,
        "is_day_before": reminder_type == ReminderType.DAY_BEFORE,
        "is_same_day": reminder_type == ReminderType.SAME_DAY,
        "is_two_hours_before": reminder_type == ReminderType.TWO_HOURS_BEFORE,
    }

    try:
        subject = render_to_string(
            "notifications/emails/visit_reminder_subject.txt",
            context,
        ).strip()

        text_body = render_to_string(
            "notifications/emails/visit_reminder_body.txt",
            context,
        )

        html_body = render_to_string(
            "notifications/emails/visit_reminder_body.html",
            context,
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            to=[recipient],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)

        log = _create_reminder_log(
            visit=visit,
            reminder_type=reminder_type,
            status=ReminderDeliveryStatus.SENT,
            recipient_email=recipient,
            execution_date=execution_date,
            sent_at=timezone.now(),
        )

        return True, log

    except Exception as exc:
        logger.exception(
            "Error sending visit reminder. visit_id=%s reminder_type=%s recipient=%s",
            getattr(visit, "pk", None),
            reminder_type,
            recipient,
        )

        log = _create_reminder_log(
            visit=visit,
            reminder_type=reminder_type,
            status=ReminderDeliveryStatus.FAILED,
            recipient_email=recipient,
            execution_date=execution_date,
            error_message=str(exc),
        )

        return False, log