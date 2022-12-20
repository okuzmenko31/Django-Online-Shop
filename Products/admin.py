from django.contrib import admin
from .models import ProductCategory, ProductSubCategory, Product, Reviews
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    characteristics = forms.CharField(widget=CKEditorUploadingWidget())
    full_info = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']


class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'main_category']
    list_display_links = ['id', 'name']
    list_editable = ['main_category']
    search_fields = ['name', 'main_category']


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['id', 'name', 'main_category', 'subcategory', 'article', 'status']
    list_display_links = ['id', 'name', 'article']
    list_editable = ['main_category', 'subcategory', 'status']
    search_fields = ['name', 'article']


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductSubCategory, ProductSubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Reviews, ReviewsAdmin)
