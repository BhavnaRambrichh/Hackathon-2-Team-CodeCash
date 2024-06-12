from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

class BankAppConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals