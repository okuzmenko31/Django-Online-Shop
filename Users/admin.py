from django.contrib import admin
from .models import User, UserShippingInformation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_staff']
    list_display_links = ['id', 'username']
    list_editable = ['is_staff']


@admin.register(UserShippingInformation)
class UserShippingInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id']
    list_editable = ['user']
    search_fields = ['user']
    list_filter = ['id', 'user']
