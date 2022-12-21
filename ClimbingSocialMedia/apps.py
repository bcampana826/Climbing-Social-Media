from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ClimbingSocialMedia'

    ## Override ready method in apps to initialize signals.py
    def ready(self):
        import ClimbingSocialMedia.signals