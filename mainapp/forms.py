from PIL import Image

from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import Product


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
