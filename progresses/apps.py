from django.apps import AppConfig


class ProgressesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'progresses'

    def ready(self):
        import progresses.signals
