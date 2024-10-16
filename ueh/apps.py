from django.apps import AppConfig


class UehConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ueh'



class UehConfig(AppConfig):
    name = 'ueh'

    def ready(self):
        import ueh.signals  # Importer les signaux
