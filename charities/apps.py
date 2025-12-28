from django.apps import AppConfig


class CharitiesConfig(AppConfig):
    name = 'charities'

    def ready(self):
        import charities.signals