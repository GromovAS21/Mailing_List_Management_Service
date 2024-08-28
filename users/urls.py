from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, UserDetailView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/',UserRegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>',email_verification, name='email_confirm'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/update', UserUpdateView.as_view(), name='user_update'),
]
