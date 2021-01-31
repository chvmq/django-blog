from django.contrib import admin
from .models import News, Category


class BlogAdmin(admin.ModelAdmin):
    # представление объектов в админке
    list_display = ['id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'views']
    # какие поля объекта будут отображатся

    list_display_links = ['id', 'title']
    # на какие поля обЪекта можно нажать

    search_fields = ['title', 'content']
    # по каким полям можно искать объекты

    list_editable = ['is_published']
    # какие поля можно редачить прямо из списка

    list_filter = ['is_published', 'category']
    # сайдбар фильтр справа


class CategoryAdmin(admin.ModelAdmin):
    # представление объектов в админке
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']


admin.site.register(News, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
# Добавление моделей в админку
