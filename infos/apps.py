from django.apps import AppConfig


class InfosConfig(AppConfig):
    name = 'infos'
    def ready(self):
        import infos.signals
