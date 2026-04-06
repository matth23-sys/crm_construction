from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Comando base para revisar y disparar recordatorios de visitas técnicas."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "Comando base activo. La integración real con visits/notifications se implementará en la Fase 8."
            )
        )