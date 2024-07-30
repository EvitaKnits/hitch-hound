from django.apps import AppConfig


class IssuesConfig(AppConfig):
    """ Configuration class for the 'issues' application """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'issues'

    def ready(self):
        """
        Import signals when the application is ready.
        This ensures signal handlers are connected when the application starts.
        """
        import issues.signals
