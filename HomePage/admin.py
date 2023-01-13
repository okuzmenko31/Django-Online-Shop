from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from .models import AboutUs, RecommendedProductsPhotos
from django import forms


class AboutUsForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorUploadingWidget())
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = AboutUs
        fields = '__all__'


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsForm
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'title']


@admin.register(RecommendedProductsPhotos)
class RecommendedProductsPhotos(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']
