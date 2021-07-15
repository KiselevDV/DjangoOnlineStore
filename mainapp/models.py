from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()  # settings.AUTH_USER_MODEL


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
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    image = models.ImageField(
        verbose_name='Изображение товара', upload_to='mainapp/images')
    price = models.DecimalField(
        verbose_name='Цена', max_digits=9, decimal_places=2)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Notebook(Product):
    """Ноутбук"""
    diagonal = models.CharField(verbose_name='Диагональ', max_length=255)
    display_type = models.CharField(verbose_name='Тип дисплея', max_length=255)
    processor_freq = models.CharField(
        verbose_name='Частота процессора', max_length=255)
    ram = models.CharField(verbose_name='Оперативная память', max_length=255)
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
    diagonal = models.CharField(verbose_name='Диагональ', max_length=255)
    display_type = models.CharField(verbose_name='Тип дисплея', max_length=255)
    resolution = models.CharField(
        verbose_name='Разрешение экрана', max_length=255)
    accum_volume = models.CharField(
        verbose_name='Объём батареи', max_length=255)
    ram = models.CharField(verbose_name='Оперативная память', max_length=255)
    sd = models.BooleanField(default=True)
    sd_volume = models.CharField(
        verbose_name='Максимальный объём встраиваемой памяти', max_length=255)
    main_cam_mp = models.CharField(
        verbose_name='Главная камера', max_length=255)
    front_cam_mp = models.CharField(
        verbose_name='Фронтальная камера', max_length=255)

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
