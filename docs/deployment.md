# Deployment inicial

## Producción
- usar `config.settings.production`
- definir `SECRET_KEY`
- definir `ALLOWED_HOSTS`
- definir `CSRF_TRUSTED_ORIGINS`
- definir `DATABASE_URL`
- definir backend de correo real
- ejecutar `collectstatic`
- ejecutar migraciones
- correr Gunicorn detrás de proxy reverso

## Comandos
```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application