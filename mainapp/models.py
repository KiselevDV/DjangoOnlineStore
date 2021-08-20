from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()  # settings.AUTH_USER_MODEL


class Category(models.Model):
    """Категория"""
    name = models.CharField(verbose_name='Имя категории', max_length=255)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    # def get_fields_for_filter_in_template(self):
    #     return ProductFeatures.objects.filter(
    #         category=self, use_in_filter=True
    #     ).prefetch_related('category').value(
    #         'feature_key', 'feature_measure', 'feature_name', 'filter_type')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Product(models.Model):
    """Товар"""

    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    image = models.ImageField(
        verbose_name='Изображение товара', upload_to='mainapp/images',
        null=True, blank=True)
    price = models.DecimalField(
        verbose_name='Цена', max_digits=9, decimal_places=2)
    slug = models.SlugField(unique=True)

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CartProduct(models.Model):
    """
    Продуктовая корзина - промежуточный объект.
    Объект который положим в корзину.
    """
    user = models.ForeignKey(
        'Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey(
        'Cart', verbose_name='Корзина', on_delete=models.CASCADE,
        related_name='related_products')
    product = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
    final_price = models.DecimalField(
        verbose_name='Общая цена', max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        """Подсчёт общей цены"""
        self.final_price = self.qty * self.product.price
        super(CartProduct, self).save(*args, **kwargs)

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)

    class Meta:
        verbose_name = 'Продуктовая корзина'
        verbose_name_plural = 'Продуктовые корзины'


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey(
        'Customer', verbose_name='Владелец', on_delete=models.CASCADE,
        null=True)
    products = models.ManyToManyField(
        CartProduct, verbose_name='Продукты', related_name='related_cart',
        blank=True)
    total_products = models.PositiveIntegerField(
        verbose_name='Количество уникальных товаров', default=0)
    final_price = models.DecimalField(
        verbose_name='Общая цена', default=0, max_digits=9, decimal_places=2)

    # Если данная корзина используется => закреплена за конкретным пользова
    # -телем и её может использовать, в дальнейшем, только данный пользователь
    in_order = models.BooleanField(
        verbose_name='Корзина используется', default=False)
    # Корзина 'заглушка' для неавторизованных пользователей => код не ломается
    for_anonymous_user = models.BooleanField(
        verbose_name='Пользователь авторизован', default=False)

    def __str__(self):
        return 'Корзина №{}, владелец {}'.format(
            str(self.id), self.owner)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Customer(models.Model):
    """Пользователь. Расширенная модель User"""
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(
        verbose_name='Номер телефона', max_length=20, null=True, blank=True)
    address = models.CharField(
        verbose_name='Адрес', max_length=255, null=True, blank=True)
    orders = models.ManyToManyField(
        'Order', verbose_name='Заказы покупателя',
        related_name='related_customer', blank=True)

    def __str__(self):
        return '{} ({} {})'.format(
            self.user, self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Order(models.Model):
    """Заказ товаров"""

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_PAYED = 'payed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
        (STATUS_PAYED, 'Заказ оплачен'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    cart = models.ForeignKey(
        Cart, verbose_name='Корзина', on_delete=models.CASCADE,
        null=True, blank=True)
    customer = models.ForeignKey(
        Customer, verbose_name='Покупатель', on_delete=models.CASCADE,
        related_name='related_orders')
    first_name = models.CharField(verbose_name='Имя', max_length=60)
    last_name = models.CharField(verbose_name='Фамилия', max_length=60)
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    address = models.CharField(
        verbose_name='Адрес', max_length=1024, null=True, blank=True)
    status = models.CharField(
        verbose_name='Статус заказа', max_length=15, choices=STATUS_CHOICES,
        default=STATUS_NEW)
    buying_type = models.CharField(
        verbose_name='Тип заказа', max_length=15, choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF)
    comment = models.TextField(
        verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(
        verbose_name='Дата создания заказа', auto_now=True)
    order_date = models.DateField(
        verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return 'Заказ №{}, от пользователя {}'.format(
            str(self.id), self.customer)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

# Функционал ниже реализован в отдельном приложении 'specs'
# class ProductFeatures(models.Model):
#     """Спец. хар-ки для товаров"""
#     RADIO = 'radio'
#     CHECKBOX = 'checkbox'
#
#     FILTER_TYPE_CHOICES = (
#         (RADIO, 'Радиокнопка'),
#         (CHECKBOX, 'Чекбокс')
#     )
#
#     feature_key = models.CharField(
#         verbose_name='Ключ характеристики', max_length=100)
#     feature_name = models.CharField(
#         verbose_name='Наименование', max_length=255)
#     category = models.ForeignKey(
#         Category, verbose_name='Категория', on_delete=models.CASCADE)
#     postfix_for_value = models.CharField(
#         verbose_name='Постфикс для значения', max_length=20,
#         null=True, blank=True,
#         help_text=('Например для хар-ки "Часы работы" к значению можно '
#                    'добавить постфикс "часов", и как результат - '
#                    'значение "10 часов"')
#     )
#     use_in_filter = models.BooleanField(
#         verbose_name='Использовать в фильтрации товаров в шаблоне',
#         default=False)
#     filter_type = models.CharField(
#         verbose_name='Тип фильтра', max_length=20, default=CHECKBOX,
#         choices=FILTER_TYPE_CHOICES)
#     filter_measure = models.CharField(
#         verbose_name='Единица измерения для фильтра', max_length=50,
#         help_text=('Единица измерения для конкретного фильтра. Например '
#                    '"Частота процессора (GHz)". Единицей измерения будет'
#                    'информация в скобках')
#     )
#
#     def __str__(self):
#         return (f'Категория - "{self.category.name}" | '
#                 f'Характеристика  - "{self.feature_name}"')
#
#     class Meta:
#         verbose_name = 'Характеристики для товара'
#         verbose_name_plural = 'Характеристики для товаров'
#
#
# class ProductFutureValidators(models.Model):
#     """Валидатор для спец. характеристик товаров"""
#     category = models.ForeignKey(
#         Category, verbose_name='Категория', on_delete=models.CASCADE)
#     feature = models.ForeignKey(
#         ProductFeatures, verbose_name='Характеристика',
#         on_delete=models.CASCADE, null=True, blank=True)
#     feature_value = models.CharField(
#         verbose_name='Значение характеристики', max_length=255, unique=True,
#         null=True, blank=True)
#
#     def __str__(self):
#         if not self.feature:
#             return (f'Валидатор категории "{self.category.name}" - '
#                     f'характеристика не выбрана')
#         return (f'Валидатор категории "{self.category.name}" | '
#                 f'Характеристика - "{self.feature.feature_name}" | '
#                 f'Значение - "{self.feature_value}"')
#
#     class Meta:
#         verbose_name = 'Валидатор для спец. хар-к'
#         verbose_name_plural = 'Валидаторы для спец. хар-к'
