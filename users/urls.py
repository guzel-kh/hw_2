
from django.urls import path

from users.apps import UsersConfig
from users.views import LogoutView, LoginView, RegisterView, UserUpdateView, generate_new_password, email_verification, reset_password

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('users/reset_password', reset_password, name='reset_password'),

]