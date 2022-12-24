from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .services import get_discount, get_price_sep


class ProductCategory(models.Model):
    """Model of product category, as well model of main category for subcategory"""
    title = models.CharField(max_length=200, verbose_name="Ім'я категорії в заголовку сторінки", blank=True)
    name = models.CharField(max_length=150, verbose_name="Ім'я категорії")
    slug = models.SlugField(unique=True, verbose_name="Ім'я категорії в посиланні")
    subcategory = models.ManyToManyField('ProductSubCategory', verbose_name='Підкатегорія', blank=True, db_index=True)

    def get_absolute_url(self):
        return reverse('products_by_cat', kwargs={'slug': self.slug, 'category_id': self.pk})

    def __str__(self):
        return f"ID категорії: {self.id}, ім'я категорії: {self.name}"

    class Meta:
        verbose_name = 'категорія товарів'
        verbose_name_plural = 'Категорії товарів'
        ordering = ['id']


class ProductSubCategory(models.Model):
    """Model of product subcategory"""
    title = models.CharField(max_length=200, verbose_name="Ім'я підкатегорії в заголовку сторінки", blank=True)
    name = models.CharField(max_length=150, verbose_name="Ім'я подкатегории")
    slug = models.SlugField(unique=True, verbose_name="Ім'я підкатегорії в посиланні")
    main_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Основна категорія',
                                      db_index=True)

    def get_absolute_url(self):
        return reverse('by_sub', kwargs={'category_id': self.main_category.pk, 'slug': self.slug, 'sub_id': self.pk})

    def __str__(self):
        return f"ID підкатегорії: {self.id}, ім'я підкатегорії: {self.name}"

    class Meta:
        verbose_name = 'підкатегорія товарів'
        verbose_name_plural = 'Підкатегорії товарів'


class Product(models.Model):
    """Model of product"""
    PRODUCT_STATUS_CHOICES = [
        ('Have in shop', 'Є в наявності'),
        ('Ends in shop', 'Закінчується'),
        ('Not in shop', 'Нема в наявності'),
    ]

    """Модель товаров"""
    name = models.CharField(max_length=250, verbose_name="Ім'я товару")
    characteristics = models.TextField(verbose_name='Характеристики товару', blank=True)
    full_info = models.TextField(verbose_name='Повна інформація про товар', blank=True)
    img = models.ImageField(upload_to='products_images/', verbose_name='Фото товару', blank=True)
    main_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, null=True,
                                      verbose_name='Основна категорія товару', blank=True, db_index=True)
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.PROTECT, null=True,
                                    verbose_name='Підкатегорія товару', blank=True, db_index=True)
    price = models.IntegerField(verbose_name='Вартість товару')
    discount_availability = models.BooleanField(default=False, verbose_name='Наявність знижки')
    discount = models.IntegerField(verbose_name='Знижка на товар', blank=True)
    price_with_discount = models.IntegerField(verbose_name='Вартість товару зі знижкою', default=0, blank=True)
    article = models.CharField(max_length=250, verbose_name='Артикул товару', blank=True)
    status = models.CharField(max_length=300, choices=PRODUCT_STATUS_CHOICES, default='Have in shop',
                              verbose_name='Статус наявності товару')
    slug = models.SlugField(unique=False, verbose_name="Ім'я товару в посиланні", blank=True)
    price_view = models.CharField(max_length=400,
                                  verbose_name='Відредаговане представлення ціни, яке буде бачити користувач',
                                  blank=True, default='1')
    price_with_discount_view = models.CharField(max_length=400,
                                                verbose_name='Відредаговане представлення ціни зі знижкою, '
                                                             'яке буде бачити користувач', blank=True, default='1')
    total_rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Total rating of product',
                                       default=0)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category': self.main_category.slug,
                                                 'subcategory': self.subcategory.slug,
                                                 'pk': self.pk,
                                                 'slug': self.slug})

    def __str__(self):
        if self.article:
            return f"ID товару: {self.id}, ім'я товару: {self.name}, артикул товару: {self.article}"
        else:
            return f"ID товару: {self.id}, ім'я товару: {self.name}"

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товари'
        ordering = ['-id']

    def save(self, *args, **kwargs):

        """Discount calculation"""
        if self.discount_availability:
            """If we have discount"""

            self.price_with_discount = get_discount(self.price, self.discount)

            self.price_with_discount_view = get_price_sep(self.price_with_discount)

            self.price_view = get_price_sep(self.price)

        else:
            """If we dont have discount"""
            self.price_with_discount = self.price

            self.price_view = get_price_sep(self.price)
            self.price_with_discount_view = self.price_view

        super(Product, self).save(*args, **kwargs)


class Reviews(models.Model):
    """Model of reviews"""
    name = models.CharField(max_length=200, verbose_name="Ім'я користувача", blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='review_product')
    review = models.TextField(verbose_name='Відгук')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата залишення відгуку')
    rating = models.FloatField(verbose_name='Rating', blank=True)
    ip = models.CharField(max_length=20, blank=True, verbose_name='IP address')

    def __str__(self):
        return f"Ім'я відвідувача: {self.name}, ID відгуку: {self.id}"

    class Meta:
        verbose_name = 'відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']
