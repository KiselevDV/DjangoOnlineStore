from django.urls import path

from .views import (test_view, ProductDetailView, )

app_name = 'mainapp'
urlpatterns = [
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(),
         name='product_detail'),
    path('', test_view, name='base'),
]
