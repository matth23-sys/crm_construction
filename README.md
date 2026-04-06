# CRM Construction

CRM web para empresa de construcción, desarrollado con Django bajo arquitectura de monolito modular.

## Stack base
- Django
- PostgreSQL
- Media storage local (evolucionable)
- SMTP / proveedor transaccional
- WhiteNoise para estáticos

## Entornos
- `config.settings.base`
- `config.settings.local`
- `config.settings.production`

## Primer arranque

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/local.txt
cp .env.example .env
python manage.py makemigrations users
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver