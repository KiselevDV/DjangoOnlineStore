import stripe  # система онлайн платежей

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import View, DetailView

from .forms import LoginForm, RegistrationForm, OrderForm
from .mixins import CartMixin
from .models import (Category, Product, CartProduct, Customer, Order, )
from .utils import recalc_cart


class LoginView(CartMixin, View):
    """Авторизация/регистрация пользователя"""

    def get(self, request, *args, **kwargs):
        """Получить форму"""
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'mainapp/login.html', context)

    def post(self, request, *args, **kwargs):
        """Обработать/отправить"""
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'mainapp/login.html', context)


class RegistrationView(CartMixin, View):
    """Регистранция нового пользователя"""

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'mainapp/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            Customer.objects.create(
                user=new_user, phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            # Аутентификация нового пользователя и вход на сайт
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')

        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'mainapp/registration.html', context)


class ProfileView(CartMixin, View):
    """Профиль пользователя"""

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        categories = Category.objects.all()
        context = {
            'orders': orders,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'mainapp/profile.html', context)


class BaseView(CartMixin, View):
    """Главная страница"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'mainapp/base.html', context)


class ProductDetailView(CartMixin, DetailView):
    """Детальное представление всех классов наследующихся от Product"""

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Добавить информацию о корзине"""
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, DetailView):
    """Подробный вывод категорий"""

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Добавить информацию о корзине"""
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CartView(CartMixin, View):
    """Корзина"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'cart': self.cart,
        }
        return render(request, 'mainapp/cart.html', context)


class AddToCartView(CartMixin, View):
    """Добавить товар в корзину"""

    def get(self, request, *args, **kwargs):
        # Получить текущие content type модели и слаг товара
        product_slug = kwargs.get('slug')

        # Получить продукт
        product = Product.objects.get(slug=product_slug)

        # Новый продукт, для добавления в корзину (промежуточная модель)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product)

        if created:  # только если товара нет в корзине
            # Добавить товар (cart_product) в корзину (cart)
            self.cart.products.add(cart_product)
        # Информация о корзине сохраняется только тогда,
        # когда в неё что-то добавляется
        recalc_cart(self.cart)

        messages.add_message(
            request, messages.INFO, 'Товар успешно добавлен в корзину')
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    """Удалить товар из корзины"""

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')

        product = Product.objects.get(slug=product_slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product)

        # Удалить продукт из корзины (Cart)
        self.cart.products.remove(cart_product)
        # Удалить запись из CartProduct
        cart_product.delete()

        recalc_cart(self.cart)

        messages.add_message(
            request, messages.INFO, 'Товар успешно удалён из корзины')
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    """Кол-во единиц добавляемого товара в корзине"""

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')

        product = Product.objects.get(slug=product_slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product)

        # Получить значение из form.input (name/value)
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)

        messages.add_message(request, messages.INFO, 'Кол-во успешно изменено')
        return HttpResponseRedirect('/cart/')


class CheckoutView(CartMixin, View):
    """Оформление заказа. Вывод данных на странице"""

    def get(self, request, *args, **kwargs):
        # Встраиваем систему оплаты онлайн - stripe
        # Создать инициацию онлайн платежа
        # Set your secret key. Remember to switch to your live secret key in production.
        # See your keys here: https://dashboard.stripe.com/apikeys
        stripe.api_key = "sk_test_51JOnsiC11ED4v6Z5ywujZ2DgfexY4dphHIjspYYXSQpudIJQILtZQf7cj0YNkn74mLs2ENUnhpeYT9X2qehSodIO00vuQAxNtF"

        intent = stripe.PaymentIntent.create(
            # amount - принимает только int!!!
            amount=int(self.cart.final_price * 100),
            currency='rub',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )

        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'categories': categories,
            'cart': self.cart,
            'form': form,
            # Установить/вернуть секретный ключ, для валидации оплаты
            'client_secret': intent.client_secret,
        }
        return render(request, 'mainapp/checkout.html', context)


class MakeOrderView(CartMixin, View):
    """Обработка заказа. Забрать данные из полей формы"""

    # transaction.atomic - если на любом этапе выполнения ф-ии "код сломается",
    # произойдёт аткат к началу ф-ии
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)  # приостановить сохранение

            # Забрать данные из полей формы
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()

            # Закрепить корзину за пользователем и очистить её
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart  # поместить корзину после созранения
            customer.orders.add(new_order)
            new_order.save()

            messages.add_message(
                request, messages.INFO, 'Заказ отправлен. Спасибо за покупку!')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class PayedOnlineOrderView(CartMixin, View):
    """Оплата заказа онлайн"""

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        new_order = Order()  # создать новый объект

        new_order.customer = customer
        new_order.first_name = customer.user.first_name
        new_order.last_name = customer.user.last_name
        new_order.phone = customer.phone
        new_order.address = customer.address

        # Данные из самого запроса
        new_order.buying_type = Order.BUYING_TYPE_SELF
        new_order.save()

        # Закрепить корзину за пользователем и очистить её
        self.cart.in_order = True
        self.cart.save()
        new_order.cart = self.cart  # поместить корзину после созранения
        new_order.status = Order.STATUS_PAYED
        customer.orders.add(new_order)
        new_order.save()

        return JsonResponse({'status': 'payed'})
