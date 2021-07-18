from PIL import Image

from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import Product


class NotebookAdminForm(ModelForm):
    """Изменение/расширение стандартного поведения модели Notebook в админке"""

    def __init__(self, *args, **kwargs):
        """
        Переопределение метода __init__, добавление строки help_text полю image
        """
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


class SmartphoneAdminForm(ModelForm):
    """
    Изменение/расширение стандартного поведения модели Smartphone в админке
    """

    def __init__(self, *args, **kwargs):
        super(SmartphoneAdminForm, self).__init__(*args, **kwargs)
        # Получаем экземпляр модели из kwargs
        instance = kwargs.get('instance')
        # Если есть экземпляр и поле sd=false (нет флажка), в новых экземплярах
        # по умолчанию есть (default=True), то обновить поле sd_volume_max
        if instance and not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                # Поле будет серым и только для чтения
                'readonly': True, 'style': 'background: lightgray'
            })

    def clean(self):
        # Если чекбокс 'sd' пуст (нет флажка), то
        # поле sd_volume_max тоже будет пустым
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data
