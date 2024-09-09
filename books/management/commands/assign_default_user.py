from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import ReadingMark


class Command(BaseCommand):
    help = 'Assign a default user to existing ReadingMark records'

    def handle(self, *args, **kwargs):
        default_user = User.objects.first()
        if default_user:
            ReadingMark.objects.filter(user__isnull=True).update(
                user=default_user
            )
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully assigned default user to all ReadingMark records'
                )
            )
        else:
            self.stdout.write(self.style.ERROR('No default user found'))
