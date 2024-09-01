from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания superuser'a
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@test.ru',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('Qwerty')
        user.save()

