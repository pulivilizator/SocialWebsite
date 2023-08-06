from django.contrib import admin

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'slug']
    list_filter = ['user', 'slug']
    search_fields = ['user', 'slug']
