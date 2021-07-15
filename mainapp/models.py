from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()  # settings.AUTH_USER_MODEL


class Category(models.Model):
    """Категория"""
    name = models.CharField(verbose_name='Имя категории', max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт"""
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    image = models.ImageField(verbose_name='Изображение товара')
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    """Продуктовая корзина"""
    user = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, verbose_name='Продукты', blank=True)
    total_products = models.PositiveIntegerField(
        verbose_name='Количество уникальных товаров', default=0)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.id


class Customer(models.Model):
    """Пользователь. Расширенная модель User"""
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=255)

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)


class Specifications(models.Model):
    """Спецификации"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(verbose_name='Имя товара для характеристик', max_length=255)

    def __str__(self):
        return 'Характеристики для товара: {}'.format(self.name)
