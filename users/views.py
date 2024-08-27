import secrets

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserRegisterView(CreateView):
    """
    Форма создания нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        user.save(update_fields=['is_active', 'token'])
        send_mail(
            'Подтверждение почты',
            f'Перейдите по ссылке для подтверждения почты: {url}',
            EMAIL_HOST_USER,
            [user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Перевод пользователя в статуc Активный при проходе по ссылке с почты
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save(update_fields=['is_active'])
    return redirect(reverse('users:login'))


class UserDetailView(DetailView):
    """
    Вывод информации о пользователе
    """
    model = User


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('message:message_list')

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.object.pk})
