from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания пользователей
    """

    def handle(self, *args, **options):
        user_list = [
            {"email": "test1@test.ru", "first_name": "Test1", "last_name": "Testov1"},
            {"email": "test2@test.ru", "first_name": "Test2", "last_name": "Testov2"},
            {"email": "test3@test.ru", "first_name": "Test3", "last_name": "Testov3"},
            {
                "email": "test4@test.ru",
                "first_name": "Test4",
                "last_name": "Testov4",
                "is_active": False,
            },
        ]
        user_for_create = []
        for item in user_list:
            user_for_create.append(User(**item))
            user_for_create[-1].set_password("Qwerty")

        User.objects.bulk_create(user_for_create)
