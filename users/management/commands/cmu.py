from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания профиля модератора
    """
    def handle(self, *args, **options):
        moderator = User.objects.create(
            email='moderator@test.ru',
            first_name='Moderator',
            last_name='Moderatorov',
            is_staff=True
        )
        moderator.set_password('Qwerty')
        moderator.groups.add(1)
        moderator.save()
