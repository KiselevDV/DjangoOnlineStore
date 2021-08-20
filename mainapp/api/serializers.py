from rest_framework import serializers

from ..models import Category, Customer, Order


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
