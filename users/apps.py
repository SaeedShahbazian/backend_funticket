from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _
from users.management import create_groups


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _("Users")

    def ready(self):
        post_migrate.connect(
            create_groups,
            sender=self,
            dispatch_uid="users.management.create_groups"
        )
