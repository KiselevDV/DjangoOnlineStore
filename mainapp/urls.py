from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    LoginView, RegistrationView, ProfileView, BaseView, ProductDetailView,
    CategoryDetailView, CartView, AddToCartView, DeleteFromCartView, ChangeQTYView,
    CheckoutView, MakeOrderView, PayedOnlineOrderView,
)

urlpatterns = [
    # Оформление, отправка и оплата заказа
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('payed-online-order/', PayedOnlineOrderView.as_view(),
         name='payed_online_order'),

    # Корзина. Добавление/удаление товаров. Кол-во единиц одного товара.
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(),
         name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(),
         name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),

    # Вывод всех категорий товаров
    path('category/<str:slug>/', CategoryDetailView.as_view(),
         name='category_detail'),

    # Детальное описание товара
    path('products/<str:slug>/', ProductDetailView.as_view(),
         name='product_detail'),

    # Главная страница. Авторизация, регистрация, профиль пользователя
    path('profile/', ProfileView.as_view(), name='profile'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', BaseView.as_view(), name='base'),
]
