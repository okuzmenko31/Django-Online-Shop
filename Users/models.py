from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=350, verbose_name='Name')
    last_name = models.CharField(max_length=300, verbose_name='Last name')
    surname = models.CharField(max_length=300, verbose_name='Surname')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=200, verbose_name='Phone number', blank=True)
    email_confirmed = models.BooleanField(default=False, verbose_name='Email confirmed?')
    post_office = models.CharField(max_length=20, verbose_name='Post office', blank=True)
    city = models.CharField(max_length=100, verbose_name='City or town', blank=True)
    photo = models.ImageField(upload_to='images/user', verbose_name='Photo', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'User: {self.name} {self.last_name} {self.surname}'
