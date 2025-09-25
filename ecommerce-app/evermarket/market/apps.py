from django.apps import AppConfig
from .functions.twitter import Tweet
from django.db.models.signals import post_migrate


class MarketConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "market"

    # Ready function to be run once at startup
    def ready(self):
        # Initialize Tweet class
        Tweet()
        # Import function now to avoid premature loading of function
        from .utils import setup_group_permissions

        # Initialize group permissions (after migrations)
        post_migrate.connect(
            setup_group_permissions,
            sender=self,
        )
