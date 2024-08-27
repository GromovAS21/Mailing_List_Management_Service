from django.contrib.auth.forms import UserCreationForm

from message.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
