from django.db import models
from Products.models import ProductSubcategory


class AboutUs(models.Model):
    title = models.CharField(max_length=550, verbose_name='Title', blank=True)
    text = models.TextField(verbose_name='Info', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'About us'
        verbose_name_plural = 'About us info'


class RecommendedProductsPhotos(models.Model):
    product_subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, verbose_name='Subcategory')
    photo = models.ImageField(upload_to='recommended_products/photos/', verbose_name='photo')

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'Recommended products photo'
        verbose_name_plural = 'Recommended products photos'
