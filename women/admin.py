from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    # атрибут содержит порядок и список редактируемх полей, которые нужно отображать в форме реактирования записи в
    # админ панели
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # указываем не редактируемые поля
    save_on_top = True  # Атрибут устанавливает панель сохранения вверху страницы

    def get_html_photo(self, object):
        '''Метод формирует html код для вывода миниатюры изображения в админ панели'''
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        #  функция mark_safe указывает не экранировать html теги

    get_html_photo.short_description = 'Миниатюра'  # изменяет название поля в админ панели вместо 'GET HTML PHOTO'
    # будет 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'  # заголовок страницы админ панели
admin.site.site_header = 'Админ-панель сайта о женщинах'  # Название заголовка в админ панели
