from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date
from apps.visits.services import process_due_visit_reminders

class Command(BaseCommand):
    help = "Process due technical visit reminders and send emails without duplicates."

    def add_arguments(self, parser):
        parser.add_argument("--date", dest="run_date", required=False, help="Execution date in YYYY-MM-DD format.")
        parser.add_argument("--retry-failed", action="store_true", dest="retry_failed", help="Retry failed reminder logs.")

    def handle(self, *args, **options):
        run_date = options.get("run_date")
        retry_failed = options.get("retry_failed", False)

        parsed_date = None
        if run_date:
            parsed_date = parse_date(run_date)
            if not parsed_date:
                raise CommandError("Invalid date format. Use YYYY-MM-DD.")

        summary = process_due_visit_reminders(run_date=parsed_date, retry_failed=retry_failed)

        self.stdout.write(self.style.SUCCESS(
            f"Visit reminders processed. Date={summary.get('processed_date')} "
            f"Sent={summary.get('sent', 0)} Failed={summary.get('failed', 0)} Skipped={summary.get('skipped', 0)}"
        ))