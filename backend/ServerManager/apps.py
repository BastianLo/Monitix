from django.apps import AppConfig


class ServermanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ServerManager'

    def ready(self):
        import ServerManager.signals