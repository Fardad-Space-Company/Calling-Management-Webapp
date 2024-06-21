from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
