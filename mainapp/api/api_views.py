"""
Не рендерит информацию в HTML, выдаёт данные в JSON
ListCreateAPIView - либо получить список, либо создать объект
"""
from collections import OrderedDict

from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, )
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import (
    NotebookSerializer, SmartphoneSerializer, CategorySerializer,
    CustomerSerializer, )

from ..models import Notebook, Smartphone, Category, Customer


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


class NotebookListAPIView(ListAPIView):
    """Все ноутбуки"""
    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()


class SmartphoneListAPIView(ListAPIView):
    """Все смартфоны"""
    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    # Фильтрация через бекэнд
    filter_backends = [SearchFilter]
    search_fields = ['diagonal', 'display_type']

    # # Фильтрация через переопределение работы queryset
    # def get_queryset(self):
    #     """Переопределение работы базового queryset"""
    #     qs = super().get_queryset()  # базовый queryset
    #     # http://127.0.0.1:8000/api/smartphones/?diagonal=6.1%22&display_type=OLED
    #     # Для фильтрации через QUERY параметры - query_params.get('price')
    #     # diagonal=6.1%22 и display_type=OLED - query_params
    #     diagonal, display_type = (
    #         self.request.query_params.get('diagonal'),
    #         self.request.query_params.get('display_type')
    #     )
    #     search_params = {
    #         'diagonal__iexact': diagonal,
    #         'display_type__iexact': display_type,
    #     }
    #     return qs.filter(**search_params)


class SmartphoneDetailAPIView(RetrieveAPIView):
    """Детальная информация о смартфоне"""

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    lookup_field = 'id'


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
