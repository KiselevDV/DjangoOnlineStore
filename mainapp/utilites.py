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
