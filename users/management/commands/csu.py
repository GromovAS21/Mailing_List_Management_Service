from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания superuser'a
    """
    def handle(self, *args, **options):
        user = User.objects.create(email='admin@test.ru')
        user.set_password('Qwerty')
        user.is_staff = True
        user.is_superuser = True
        user.save()

