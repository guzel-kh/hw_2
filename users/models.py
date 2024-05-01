from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=35, verbose_name="телефон", null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name="Страна")

    token = models.CharField(max_length=100, verbose_name="token", null=True, blank=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email
