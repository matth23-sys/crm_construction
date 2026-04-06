import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.exceptions import NotificationError
from core.utils.emails import normalize_recipients, prefix_subject

logger = logging.getLogger("crm.notifications")


def send_system_email(
    *,
    subject,
    to,
    body="",
    html_template=None,
    context=None,
    cc=None,
    bcc=None,
    from_email=None,
    fail_silently=False,
):
    """
    Servicio base de correo reutilizable por visits, notifications y otros módulos.
    """
    recipients = normalize_recipients(to)
    cc = normalize_recipients(cc)
    bcc = normalize_recipients(bcc)
    context = context or {}

    if not recipients:
        raise NotificationError("No se proporcionaron destinatarios para el correo.")

    final_subject = prefix_subject(subject)

    html_body = None
    text_body = body or ""

    if html_template:
        html_body = render_to_string(html_template, context)
        if not text_body:
            text_body = context.get("plain_body", "")

    message = EmailMultiAlternatives(
        subject=final_subject,
        body=text_body,
        from_email=from_email,
        to=recipients,
        cc=cc,
        bcc=bcc,
    )

    if html_body:
        message.attach_alternative(html_body, "text/html")

    try:
        result = message.send(fail_silently=fail_silently)
        logger.info("email_sent subject=%s recipients=%s", final_subject, recipients)
        return result
    except Exception as exc:
        logger.exception("email_send_failed subject=%s recipients=%s", final_subject, recipients)
        if fail_silently:
            return 0
        raise NotificationError("Ocurrió un error al enviar el correo.") from exc