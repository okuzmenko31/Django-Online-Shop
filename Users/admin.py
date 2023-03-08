from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_staff']
    list_display_links = ['id', 'username']
    list_editable = ['is_staff']
