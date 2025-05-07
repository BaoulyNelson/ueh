from django.apps import AppConfig


class bunexeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bunexe'



class bunexeConfig(AppConfig):
    name = 'bunexe'

    def ready(self):
        import bunexe.signals  # Importer les signaux
