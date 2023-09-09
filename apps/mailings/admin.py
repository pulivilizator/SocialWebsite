from django.contrib import admin

from .models import *

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "active"]
    list_filter = ["user", "date", "active"]
    search_fields = ["user"]
    
