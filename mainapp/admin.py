"""
ModelChoiceField - встроеная модель выбора
mark_safe - превращает обычную строку в HTML тег
"""
from PIL import Image

from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import Category, Product, Notebook, Smartphone, CartProduct, Cart, Customer


class NotebookAdminForm(ModelForm):
    """Переопределение/расширение логики модели Notebook"""

    def __init__(self, *args, **kwargs):
        """Добавление строки help_text полю image"""
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size:14px;">'
            'Загружайте изображения с минимальным разрешением - {}x{}. '
            'При загрузке изображения более {}x{} оно будет обрезано!'
            '</span>'.format(*Product.MIN_VALID_RESOLUTION,
                             *Product.MAX_VALID_RESOLUTION)
        )

    def clean_image(self):
        """
        Получение данных поля 'image' и их валидация. Данная логика
        осуществляется на уровне формы в админке (не в моделях/shell ...)
        """

        image = self.cleaned_data['image']
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError(
                'Размер изображения не должен превышать 10 Мб')
        # т.к. данный тип медиафайл, данные в виде стрима (нет ширины/высоты)
        # => работаем с экземрляром библиотеки PIL

        # экземпляр img наследует поля класса Image => размер - ширина/высота
        img = Image.open(image)
        min_height, min_width = Product.MIN_VALID_RESOLUTION
        # max_height, max_width = Product.MAX_VALID_RESOLUTION
        # img.width/img.height - ширина и высота объекта image
        if img.height < min_height or img.width < min_width:
            raise ValidationError(
                'Разрешение изображения меньше минимального!')
        # if img.height > max_height or img.width > max_width:
        #     raise ValidationError(
        #         'Разрешение изображения больше максимального!')

        return image


class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm

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
            return ModelChoiceField(
                Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey()


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)

admin.site.site_header = 'Интернет магазин'
admin.site.site_title = 'Сайт интернет магазина'
