from django.apps import AppConfig


class CoreTenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_tenant'

    def ready(self):
        import core_tenant.signals  # Adjust the import to your signals module