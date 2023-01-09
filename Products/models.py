from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .services import get_discount, get_price_sep, get_rating_star


class ProductCategory(models.Model):
    """Model of product category, as well model of main category for subcategory"""
    title = models.CharField(max_length=200, verbose_name="Ім'я категорії в заголовку сторінки", blank=True)
    name = models.CharField(max_length=150, verbose_name="Ім'я категорії")
    slug = models.SlugField(unique=True, verbose_name="Ім'я категорії в посиланні")
    subcategory = models.ManyToManyField('ProductSubCategory', verbose_name='Підкатегорія', blank=True, db_index=True)

    def get_absolute_url(self):
        return reverse('products_by_cat', kwargs={'slug': self.slug, 'category_id': self.pk})

    def __str__(self):
        return f"Категорія: {self.name}"

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
        return f"Підкатегорія: {self.name}"

    class Meta:
        verbose_name = 'підкатегорія товарів'
        verbose_name_plural = 'Підкатегорії товарів'


class ProductMemoryCategory(models.Model):
    memory_size = models.CharField(max_length=250, verbose_name='Size of memory', blank=True)
    int_memory_value = models.IntegerField(verbose_name='Value of memory size', blank=True)

    def __str__(self):
        return f'Memory size: {self.memory_size}'

    class Meta:
        verbose_name = 'Product memory category'
        verbose_name_plural = 'Product memory categories'

    def save(self, *args, **kwargs):
        if str(self.int_memory_value) in self.memory_size:
            self.memory_size = self.memory_size
        else:
            if self.int_memory_value == 1000:
                self.memory_size = f'{1}TB'
            else:
                self.memory_size = f'{self.int_memory_value}GB'
        super(ProductMemoryCategory, self).save(*args, **kwargs)


class ProductVersion(models.Model):
    title = models.CharField(max_length=250, verbose_name='Product version', blank=True)

    def __str__(self):
        return f'Version: {self.title}'

    class Meta:
        verbose_name = 'Product version category'
        verbose_name_plural = 'Product versions categories'


class ProductColorCategory(models.Model):
    color_in_admin_panel = models.CharField(max_length=350, verbose_name='Product color in admin panel', blank=True)
    color = models.CharField(max_length=350, verbose_name='Product color')
    color_hex = models.CharField(max_length=350, verbose_name='Product HEX color', blank=True)

    def __str__(self):
        return f'Color: {self.color_in_admin_panel}'

    class Meta:
        verbose_name = 'Color category'
        verbose_name_plural = 'Color categories'


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
    discount = models.IntegerField(verbose_name='Знижка на товар', blank=True, default=1)
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
    product_memory = models.ForeignKey(ProductMemoryCategory, on_delete=models.CASCADE, null=True,
                                       verbose_name='Product memory size', related_name='product_memory', blank=True)
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, null=True,
                                        verbose_name='Product esim or global', related_name='product_esim_glob',
                                        blank=True)
    product_color = models.ForeignKey(ProductColorCategory, on_delete=models.CASCADE, null=True,
                                      verbose_name='Product color', related_name='product_color', blank=True)
    editing = models.BooleanField(default=False,
                                  verbose_name='Dont touch this field, after saving it will be True.')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category': self.main_category.slug,
                                                 'subcategory': self.subcategory.slug,
                                                 'pk': self.pk,
                                                 'slug': self.slug})

    def __str__(self):
        if self.article:
            return f"{self.name}"
        else:
            return f"{self.name}"

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

    def get_star(self):
        return get_rating_star(self.total_rating)


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

    def get_review_star(self):
        return get_rating_star(self.rating)


class ProductColorChoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, verbose_name='Товар',
                                related_name='product')
    category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, db_index=True, verbose_name='Category')
    color = models.CharField(max_length=250, verbose_name='Color name at the choice button')
    memory = models.ForeignKey(ProductMemoryCategory, on_delete=models.CASCADE, db_index=True,
                               verbose_name='Product memory size', null=True, blank=True)
    version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, db_index=True,
                                verbose_name='Product esim or global', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Is active?')
    background_color = models.CharField(max_length=250, verbose_name='Button background color', blank=True)

    def __str__(self):
        return f'Color: {self.color}'

    class Meta:
        verbose_name = 'Color choice'
        verbose_name_plural = 'Colors choices'


class ProductMemoryChoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, verbose_name='Товар',
                                related_name='memory_product')
    category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, db_index=True, verbose_name='Category')
    color = models.ForeignKey(ProductColorCategory, on_delete=models.CASCADE, db_index=True,
                              verbose_name='Product color', null=True, blank=True)
    memory = models.CharField(max_length=250, verbose_name='Memory at the choice button', blank=True)
    version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, db_index=True, verbose_name='Версія товару',
                                null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активний?')

    def __str__(self):
        return f'Memory: {self.memory}'

    class Meta:
        verbose_name = "Вибір розміру пам'яті"
        verbose_name_plural = "Вибір розмірів пам'яті"


class ProductVersionChoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, verbose_name='Товар',
                                related_name='version_product')
    category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, db_index=True,
                                 verbose_name='Підкатегорія товару')
    memory = models.ForeignKey(ProductMemoryCategory, on_delete=models.CASCADE, db_index=True,
                               verbose_name="Обсяг пам'яті товару", null=True, blank=True)
    color = models.ForeignKey(ProductColorCategory, on_delete=models.CASCADE, db_index=True,
                              verbose_name='Колір товару', null=True, blank=True)
    version = models.CharField(max_length=300, verbose_name='Версія товару')
    is_active = models.BooleanField(default=True, verbose_name='Активна?')

    def __str__(self):
        return f'Версія: {self.memory}'

    class Meta:
        verbose_name = 'Вибір версії товару'
        verbose_name_plural = 'Вибір версій товару'
