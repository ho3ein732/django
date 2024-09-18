from django.contrib import admin
from .models import Blog, BlogCategory

# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'slug', 'author',
                    'created', 'updated', 'is_active']



@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created']
