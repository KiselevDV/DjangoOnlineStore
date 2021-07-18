from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone

register = template.Library()

# Шаблон HTML для рендера, генерации таблиц
TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """
TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """
TABLE_TAIl = """
                  </tbody>
                </table>
             """

# Словаь с данными для генерации HTML, контекст
PRODUCT_SPEC = {
    'notebook': {
        'Диагональ экрана': 'diagonal',
        'Технология экрана': 'display_type',
        'Тактовая частота процессора': 'processor_freq',
        'Объём оперативной памяти': 'ram',
        'Видеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge',
    },
    'smartphone': {
        'Размер экрана': 'diagonal',
        'Разрешение экрана': 'resolution',
        'Технология экрана': 'display_type',
        'Оперативная память': 'ram',
        'Наличие слота для SD карты': 'sd',
        'Максимальный объём SD карты': 'sd_volume_max',
        'Главная камера': 'main_cam_mp',
        'Фронтальная камера': 'front_cam_mp',
        'Объём батареи': 'accum_volume',
    },
}


def get_product_spec(product, model_name):
    """Формирование HTML под данную модель"""
    table_content = ''
    for key, value in PRODUCT_SPEC[model_name].items():
        # product = 'smartphone', key='Размер экрана', value = 'diagonal'
        table_content += TABLE_CONTENT.format(
            name=key, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product, arg='Что-то ещё'):
    """Генерация HTML шаблона с хар-ми в виде фильтра, через темплейт тег"""
    # print(arg)

    # Узнаём имя конкретной модели, 'product' получаем из HTML, в HTML
    # из context_object_name = 'product' (ProductDetailView)
    model_name = product.__class__._meta.model_name

    # Если данный экземпляр является объектом Smartphone, то из
    # PRODUCT_SPEC удаляем поле sd_volume_max
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем SD карты', None)
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объем SD карты'] = 'sd_volume_max'

    return mark_safe(
        TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIl)
