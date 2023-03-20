import uuid
import django.utils.timezone
from django.contrib.auth import get_user_model
from django.db import models
from Products.models import ProductSubcategory
from .services import generate_end_date

User = get_user_model()


class Coupons(models.Model):
    coupon_id = models.UUIDField(default=uuid.uuid4,
                                 editable=False,
                                 unique=True,
                                 verbose_name='Unique coupon ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner')
    subcategory = models.ForeignKey(ProductSubcategory,
                                    on_delete=models.CASCADE,
                                    verbose_name='Subcategory of products where will be discount')
    valid_from = models.DateField(verbose_name='Valid from', default=django.utils.timezone.now)
    valid_to = models.DateField('Valid to', blank=True)
    discount = models.IntegerField(default=0, verbose_name='Discount')
    is_active = models.BooleanField(default=True, verbose_name='Is active')

    class Meta:
        verbose_name = 'coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return f'Coupon for subcategory: {self.subcategory.name}'

    def save(self, *args, **kwargs):
        self.valid_to = generate_end_date(self.valid_from)
        return super(Coupons, self).save(*args, **kwargs)
