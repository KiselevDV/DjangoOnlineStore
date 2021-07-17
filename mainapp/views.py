from django.shortcuts import render
from django.views.generic import DetailView

from .models import Notebook, Smartphone


def test_view(request):
    return render(request, 'mainapp/base.html', {})


class ProductDetailView(DetailView):
    """Детальное представление всех классов наследующихся от Product"""

    # Все модели наследуемые от Product
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        """Определим конкретную модель и queryset для данного случая из kwargs"""
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'
