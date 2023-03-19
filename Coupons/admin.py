from django.contrib import admin
from .models import Coupons


@admin.register(Coupons)
class CouponsAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'subcategory', 'discount']
    list_display_links = ['id', 'discount']
    search_fields = ['user', 'subcategory']
    list_editable = ['subcategory']
    list_filter = ['subcategory']

