from django.core.management.base import BaseCommand
from event.models import Role


class Command(BaseCommand):
    help = "Import Person Role from MySql"

    def handle(self, *args, **kwargs):
        toto_success = 0

        role_lis = [
            'بازیگر',
            'کارگردان',
            'صدا پیشه',
            'مدیر دوبلاژ',
        ]

        for row_role in role_lis:
            row_role = row_role.strip()
            if not Role.objects.filter(name=row_role).exists():
                Role.objects.create(
                    name=row_role
                )
                toto_success = toto_success + 1

        # Info Command
        print("=====================================")
        print(F"[Info] Total Insert Success: {toto_success}")
