"""
ModelChoiceField - встроеная модель выбора
"""

from django.contrib import admin
from django.forms import ModelChoiceField

from .models import Category, Notebook, Smartphone, CartProduct, Cart, Customer


class NotebookAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Переопределяем работу полей связанных по Foreignkey"""
        if db_field.name == 'category':
            # Если поле является категорией, то выбрать можно только ноутбуки
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super(NotebookAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)  # стандартная работа метода


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Переопределяем работу полей связанных по Foreignkey"""
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey()


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)

admin.site.site_header = 'Интернет магазин'
admin.site.site_title = 'Сайт интернет магазина'
