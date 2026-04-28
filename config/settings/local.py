from .base import *  # noqa

DEBUG = True

# Configuración SMTP real para SiteGround
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.roofingprolegacycorp.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'no-reply-crm@roofingprolegacycorp.com'
EMAIL_HOST_PASSWORD = 'LuisG2025$$'
DEFAULT_FROM_EMAIL = 'no-reply-crm@roofingprolegacycorp.com'
SERVER_EMAIL = 'no-reply-crm@roofingprolegacycorp.com'

# Opcional pero muy recomendado: URL base del sitio para enlaces en correos
SITE_URL = 'https://roofingprolegacycorp.com'   # o https si tienes SSL instalado