from io import BytesIO
from PIL import Image
from sys import getsizeof

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from .exceptions import MinResolutionErrorException, MaxResolutionErrorException

User = get_user_model()  # settings.AUTH_USER_MODEL


class LatestProductsManager:
    """Кастомный менеджер для вывода товаров"""

    def get_products_for_main_page(self, *args, **kwargs):
        """Получение последних товаров,- args - смартфоны, ноутбуки"""
        # with_respect_to - определяет приоритет/очередности при выдаче
        # результата. Получение моделей и их запись в переменную
        with_respect_to = kwargs.get('with_respect_to')

        products = []
        # args - зарегистрированные модели в models.py
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            # ct_model - объект ContentType, model_class - родная модель,
            # _base_manager - базовый менеджер типа objects
            model_products = \
                ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)

        if with_respect_to:
            # Проверка, есть ли в этой моделе with_respect_to
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():  # queryset - если есть
                if with_respect_to in args:  # существует ли данная модель
                    # products - инстансы моделей, _meta мета атрибут
                    # экземпляров классов, model_name - название моделей
                    return sorted(
                        products,
                        key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                        reverse=True)

        return products


class LatestProducts:
    """
    Вывод последних товаров без привязки к конкретной модели.
    LatestProductsManager - менеджер от ContentType -
    позволяет работать с любой моделью
    """
    objects = LatestProductsManager()


class Category(models.Model):
    """Категория"""
    name = models.CharField(verbose_name='Имя категории', max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Продукт. Абстрактный класс"""

    # Константы для валидации размеров картинок
    MIN_VALID_RESOLUTION = (400, 400)
    MAX_VALID_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 10485760  # 10 Mb

    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    image = models.ImageField(
        verbose_name='Изображение товара', upload_to='mainapp/images')
    price = models.DecimalField(
        verbose_name='Цена', max_digits=9, decimal_places=2)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """
        Осуществление манипуляций с данными модели, перед их
        сохранением. Проверка заружаемого изображения в поле image,
        на соответствие заданным размерам.
        """
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_VALID_RESOLUTION
        # max_height, max_width = self.MAX_VALID_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException(
                'Разрешение изображения меньше минимального!')
        # if img.height > max_height or img.width > max_width:
        #     raise MaxResolutionErrorException(
        #         'Разрешение изображения больше максимального!')

        """
        Принудительная обрезка загружаемого изображения 'image', 
        если его размеры превышают MAX_VALID_RESOLUTION
        """
        new_img = img.convert('RGB')  # перед изменением из RGBA в RGB
        resized_new_img = new_img.resize((600, 600), Image.ANTIALIAS)
        # Способ №2. Не resize, а new_img.thumbnail()
        # Превращение изображения в поток данных
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', getsizeof(filestream), None
        )
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Notebook(Product):
    """Ноутбук"""
    diagonal = models.CharField(
        verbose_name='Диагональ экрана', max_length=255)
    display_type = models.CharField(
        verbose_name='Технология экрана', max_length=255)
    processor_freq = models.CharField(
        verbose_name='Тактовая частота процессора', max_length=255)
    ram = models.CharField(
        verbose_name='Объём оперативной памяти', max_length=255)
    video = models.CharField(verbose_name='Видеокарта', max_length=255)
    time_without_charge = models.CharField(
        verbose_name='Время работы аккумулятора', max_length=255)

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'


class Smartphone(Product):
    """Смартфон"""
    diagonal = models.CharField(verbose_name='Размер экрана', max_length=255)
    resolution = models.CharField(
        verbose_name='Разрешение экрана', max_length=255)
    display_type = models.CharField(
        verbose_name='Технология экрана', max_length=255)
    ram = models.CharField(verbose_name='Оперативная память', max_length=255)
    sd = models.BooleanField(verbose_name='Наличие SD карты', default=True)
    sd_volume = models.CharField(
        verbose_name='Максимальный объём встраиваемой памяти', max_length=255)
    main_cam_mp = models.CharField(
        verbose_name='Главная камера', max_length=255)
    front_cam_mp = models.CharField(
        verbose_name='Фронтальная камера', max_length=255)
    accum_volume = models.CharField(
        verbose_name='Объём батареи', max_length=255)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'


class CartProduct(models.Model):
    """Продуктовая корзина"""
    user = models.ForeignKey(
        'Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey(
        'Cart', verbose_name='Корзина', on_delete=models.CASCADE,
        related_name='related_products')
    qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
    final_price = models.DecimalField(
        verbose_name='Общая цена', max_digits=9, decimal_places=2)

    # ContentType - видит все модели, предоставляет возможность работы с ними
    # object_id - id для данной модели, content_object - их связь
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)

    class Meta:
        verbose_name = 'Продуктовая корзина'
        verbose_name_plural = 'Продуктовые корзины'


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey(
        'Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct, verbose_name='Продукты', related_name='related_cart',
        blank=True)
    total_products = models.PositiveIntegerField(
        verbose_name='Количество уникальных товаров', default=0)
    final_price = models.DecimalField(
        verbose_name='Общая цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Customer(models.Model):
    """Пользователь. Расширенная модель User"""
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=255)

    def __str__(self):
        return 'Покупатель: {} {}'.format(
            self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
