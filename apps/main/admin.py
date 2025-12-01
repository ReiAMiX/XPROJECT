from django.contrib import admin

from .models import Category, Post, PostPhoto


class PostPhotoInline(admin.TabularInline):
    model = PostPhoto


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'views_qty', 'author', 'category', 'created_at']
    list_display_links = ['id', 'name']
    list_editable = ['author', 'category']
    list_filter = ['author', 'category', 'created_at']
    readonly_fields = ['views_qty']
    search_fields = ['name']
    inlines = [PostPhotoInline]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)