from django.contrib import admin

from .models import (
    Category, Product, CartProduct, Cart, Customer, Order)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)

admin.site.site_header = 'Интернет магазин'
admin.site.site_title = 'Сайт интернет магазина'
