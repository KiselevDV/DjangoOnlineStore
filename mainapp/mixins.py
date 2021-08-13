from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from .models import Category, Cart, Customer


class CategoryDetailMixin(SingleObjectMixin):
    """Для вывода информации по категориям"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = \
            Category.objects.get_categories_for_left_sidebar()
        return context


class CartMixin(View):
    """Генерация новой корзины либо поиск уже имеющейся"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:  # создание нового пользователя
                customer = Customer.objects.create(user=request.user)

            # Процесс поиска или создания корзины
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:  # создание новой
                cart = Cart.objects.create(owner=customer)
        else:  # корзина для неавторизованного пользователя (заглушка)
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:  # создание новой
                cart = Cart.objects.create(for_anonymous_user=True)

        self.cart = cart
        return super(CartMixin, self).dispatch(request, *args, **kwargs)
