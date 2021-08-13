from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, DetailView

from .mixins import CategoryDetailMixin, CartMixin
from .models import (
    LatestProducts, Category, Notebook, Smartphone, CartProduct, Cart,
    Customer, )


class BaseView(CartMixin, View):
    """Главная страница"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone')
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'mainapp/base.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    """Детальное представление всех классов наследующихся от Product"""

    # Все модели наследуемые от Product
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        """
        Определим конкретную модель и queryset для данного случая из kwargs
        """
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Добавить информацию о конкретной модели"""
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    """Подробный вывод категорий"""

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'


class CartView(CartMixin, View):
    """Корзина"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'categories': categories,
            'cart': self.cart,
        }
        return render(request, 'mainapp/cart.html', context)


class AddToCartView(CartMixin, View):
    """Добавить товар в корзину"""

    def get(self, request, *args, **kwargs):
        # Получить текущие content type модели и слаг товара
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')

        # Получить продукт
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)

        # Новый продукт, для добавления в корзину (промежуточная модель)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart,
            content_type=content_type, object_id=product.id,
        )

        if created:  # только если товара нет в корзине
            # Добавить товар (cart_product) в корзину (cart)
            self.cart.products.add(cart_product)
        # Информация о корзине сохраняется только тогда, когда в неё что-то добавляется
        self.cart.save()

        messages.add_message(request, messages.INFO, 'Товар успешно добавлен в корзину')
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    """Удалить товар из корзины"""

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')

        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart,
            content_type=content_type, object_id=product.id,
        )

        # Удалить продукт из корзины (Cart)
        self.cart.products.remove(cart_product)
        # Удалить запись из CartProduct
        cart_product.delete()

        self.cart.save()

        messages.add_message(request, messages.INFO, 'Товар успешно удалён из корзины')
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    """Кол-во единиц добавляемого товара в корзине"""

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')

        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart,
            content_type=content_type, object_id=product.id,
        )

        # Получить значение из form.input (name/value)
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        self.cart.save()

        messages.add_message(request, messages.INFO, 'Кол-во успешно изменено')
        return HttpResponseRedirect('/cart/')
