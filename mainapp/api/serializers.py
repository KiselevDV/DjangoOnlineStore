"""
serializers.py, для валидации отсылаемой информации
PrimaryKeyRelatedField, для полей ForeignKey
required=True - если поле обязательное (в моделях)
"""

from rest_framework import serializers

from ..models import Notebook, Smartphone, Category, Customer, Order


class BaseProductSerializer:
    """Базовый сериализатор для продуктов. Абстрактный сериализатор"""
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    price = serializers.DecimalField(
        required=True, max_digits=9, decimal_places=2)
    slug = serializers.SlugField(required=True)


class NotebookSerializer(BaseProductSerializer, serializers.ModelSerializer):
    """Сериализатор для Ноутбуков"""

    diagonal = serializers.CharField(required=True)
    display_type = serializers.CharField(required=True)
    processor_freq = serializers.CharField(required=True)
    ram = serializers.CharField(required=True)
    video = serializers.CharField(required=True)
    time_without_charge = serializers.CharField(required=True)

    class Meta:
        model = Notebook
        fields = '__all__'


class SmartphoneSerializer(BaseProductSerializer, serializers.ModelSerializer):
    """Сериализатор для Смартфонов"""

    diagonal = serializers.CharField(required=True)
    resolution = serializers.CharField(required=True)
    display_type = serializers.CharField(required=True)
    ram = serializers.CharField(required=True)
    sd = serializers.BooleanField(required=True)
    sd_volume_max = serializers.CharField(required=True)
    main_cam_mp = serializers.CharField(required=True)
    front_cam_mp = serializers.CharField(required=True)
    accum_volume = serializers.CharField(required=True)

    class Meta:
        model = Smartphone
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Категорий"""
    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказов. Для расширения - получения детальной
    информации при использовании сериализатора CustomerSerializer
    """

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""

    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'
