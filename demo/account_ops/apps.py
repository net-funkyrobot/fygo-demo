from django.apps import AppConfig


class AccountOpsConfig(AppConfig):
    name = "account_ops"

    def ready(self):
        import account_ops.signals  # noqa
