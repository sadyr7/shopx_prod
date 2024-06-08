from django.apps import AppConfig


class AppVipConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_vip"

    def ready(self):
        import app_vip.signals