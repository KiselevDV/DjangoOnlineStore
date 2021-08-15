from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from .models import (
    Category, Cart, Customer, Notebook, Smartphone, Computer, Monitor, TV,
    Tablet, )


class CategoryDetailMixin(SingleObjectMixin):
    """Для вывода информации по категориям"""

    CATEGORY_SLUG2PRODUCT_MODEL = {
        'notebooks': Notebook,
        'smartphones': Smartphone,
        'computers': Computer,
        'monitors': Monitor,
        'tv_sets': TV,
        'tablets': Tablet,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получить конкретную модель (наследуемую от Products)
        # get_object() - получить инстанс категории, slug из urls
        # model = Notebook/Smartphone/... все значения модели Category
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context['category_products'] = model.objects.all()

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
