from django.urls import path

from .views import (
    BaseView, ProductDetailView, CategoryDetailView, CartView, AddToCartView,
    DeleteFromCartView, ChangeQTYView, CheckoutView, MakeOrderView,
    PayedOnlineOrderView, )

urlpatterns = [
    # Оформление, отправка и оплата заказа
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('payed-online-order/', PayedOnlineOrderView.as_view(),
         name='payed_online_order'),

    # Корзина. Добавление/удаление товаров. Кол-во единиц одного товара.
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(),
         name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/',
         DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(),
         name='change_qty'),

    # Вывод всех категорий товаров
    path('category/<str:slug>/', CategoryDetailView.as_view(),
         name='category_detail'),
    # Детальное описание товара
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(),
         name='product_detail'),
    path('', BaseView.as_view(), name='base'),
]
