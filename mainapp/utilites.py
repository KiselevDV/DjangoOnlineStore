from django.db import models
from django.urls import reverse


def get_product_url(obj, view_name):
    """
    Генерирование url-а к любой, наследуемой, модели от Product
    и рендер этих поделей по одному шаблону product_detail
    """
    # obj - передоваемая модель из get_absolute_url
    ct_model = obj.__class__._meta.model_name
    # Реверс на url view_name - (name='product_detail'), с аргументами kwargs
    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': obj.slug})


def get_models_for_count(*model_names):
    """Посчитать все инстанции на переданные модели"""
    return [models.Count(model_name) for model_name in model_names]
