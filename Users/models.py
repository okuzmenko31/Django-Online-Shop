from django.db import models
from django.contrib.auth.models import AbstractUser
from .services import get_clean_email


class User(AbstractUser):
    """User model"""
    username = models.CharField(max_length=205, verbose_name='Username', blank=True)
    name = models.CharField(max_length=350, verbose_name='Name', blank=True)
    last_name = models.CharField(max_length=300, verbose_name='Last name', blank=True)
    surname = models.CharField(max_length=300, verbose_name='Surname', blank=True)
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=200, verbose_name='Phone number', blank=True)
    bonuses_balance = models.IntegerField(verbose_name='Bonuses balance', default=0)
    bonuses_balance_usd = models.IntegerField(verbose_name='Bonuses balance in usd', default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'last_name', 'surname']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'User: {self.name} {self.last_name} {self.surname}'

    def save(self, *args, **kwargs):
        self.username = get_clean_email(self.email)
        return super().save(*args, **kwargs)


class UserShippingInformation(models.Model):
    """Shipping information model"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='User',
                             related_name='shipping_info',
                             null=True,
                             blank=True)
    country = models.CharField(max_length=250, verbose_name='Country', blank=True)
    city = models.CharField(max_length=100, verbose_name='City or town', blank=True)
    post_office = models.CharField(max_length=20, verbose_name='Post office', blank=True)

    class Meta:
        verbose_name = 'info'
        verbose_name_plural = 'Shipping infos'

    def __str__(self):
        return f'User {self.user} shipping info'
