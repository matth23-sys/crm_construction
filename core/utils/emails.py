def normalize_recipients(recipients):
    if not recipients:
        return []

    if isinstance(recipients, str):
        return [recipients]

    return [email for email in recipients if email]


def prefix_subject(subject, prefix="[CRM]"):
    subject = subject.strip()
    return f"{prefix} {subject}" if subject else prefix