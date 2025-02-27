from django.apps import AppConfig


class UserAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_auth'
    verbose_name="Manage User's Accounts"

    def ready(self):
        import user_auth.signals  