from django.contrib import admin

from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'created', 'publish', 'slug', 'status', 'author', 'photo']
    list_filter = ['title', 'publish', 'created', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish', 'title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'created', 'active', 'post', 'author']
    list_filter = ['content', 'created', 'active', 'post', 'author']
    search_fields = ['content']
    ordering = ['created']
    date_hierarchy = 'created'