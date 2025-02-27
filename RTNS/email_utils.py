from core.models import EmailConfiguration
from django.conf import settings
def get_email_configuration():
    configuration = EmailConfiguration.objects.first()
    if configuration:
        return {
            'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
            'EMAIL_HOST': configuration.smtp_host,
            'EMAIL_PORT': configuration.smtp_port,
            'EMAIL_HOST_USER': configuration.admin_email,
            'EMAIL_HOST_PASSWORD': configuration.password,
            'EMAIL_USE_TLS': True,
            'ADMIN_EMAIL': configuration.admin_email,
        }
    else:
        return {
            
        }

settings.EMAIL_CONFIG = get_email_configuration()
settings.EMAIL_BACKEND = settings.EMAIL_CONFIG.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
settings.EMAIL_HOST = settings.EMAIL_CONFIG.get('EMAIL_HOST', 'localhost')
settings.EMAIL_PORT = settings.EMAIL_CONFIG.get('EMAIL_PORT', 587)
settings.EMAIL_HOST_USER = settings.EMAIL_CONFIG.get('EMAIL_HOST_USER', '')
settings.EMAIL_HOST_PASSWORD = settings.EMAIL_CONFIG.get('EMAIL_HOST_PASSWORD', '')
settings.EMAIL_USE_TLS = settings.EMAIL_CONFIG.get('EMAIL_USE_TLS', True)

ADMIN_EMAIL = settings.EMAIL_CONFIG['ADMIN_EMAIL']