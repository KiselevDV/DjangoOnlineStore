from collections import OrderedDict

from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, )
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import CategorySerializer, CustomerSerializer

from ..models import Category, Customer


class CategoryPagination(PageNumberPagination):
    """Локальная пагинация для CategoryListAPIView"""

    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        """Кастомный метод пагинации"""
        return Response(OrderedDict([
            ('object_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('items', data)
        ]))


class CategoryAPIView(ListCreateAPIView, RetrieveUpdateAPIView):
    """Создание новой категории и их изменение"""
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    queryset = Category.objects.all()
    lookup_field = 'id'


class CustomersListAPIView(ListAPIView):
    """Все пользователи"""

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
