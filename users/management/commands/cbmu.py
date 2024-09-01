from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from users.models import User


class Command(BaseCommand):
    """
    Команда для создания blog-менеджера
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='blog-manager@test.ru',
            first_name='Blog',
            last_name='Blogov',
            is_staff=True,
        )
        permission_list = ['Can view Блог', 'Can add Блог', 'Can change Блог', 'Can delete Блог']
        for item in permission_list:
            permission = Permission.objects.get(name=item)
            user.user_permissions.add(permission)
        user.set_password('Qwerty')
        user.save()