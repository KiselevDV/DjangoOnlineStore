from django.urls import path

from .api_views import (
    NotebookListAPIView, SmartphoneListAPIView, SmartphoneDetailAPIView,
    CategoryAPIView, CustomersListAPIView, )

urlpatterns = [
    path('notebooks/', NotebookListAPIView.as_view(), name='notebooks_list'),
    path('smartphones/<str:id>/', SmartphoneDetailAPIView.as_view(),
         name='smartphone_detail'),
    path('smartphones/', SmartphoneListAPIView.as_view(),
         name='smartphones_list'),

    path('categories/<str:id>/', CategoryAPIView.as_view(),
         name='category_list'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list'),
]
