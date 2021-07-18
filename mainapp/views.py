from django.shortcuts import render
from django.views.generic import View, DetailView

from .mixins import CategoryDetailMixin
from .models import Category, Notebook, Smartphone, LatestProducts


class BaseView(View):
    """Главная страница"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone')
        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'mainapp/base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):
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


class CategoryDetailView(CategoryDetailMixin, DetailView):
    """Подробный вывод категорий"""

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'
