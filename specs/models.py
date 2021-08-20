from django.db import models


class CategoryFeature(models.Model):
    """Характеристика конкретной категории"""
    category = models.ForeignKey(
        'mainapp.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_name = models.CharField(
        verbose_name='Имя характеристики', max_length=100)
    # Для поиска в категориях через query параметры
    feature_filter_name = models.CharField(
        verbose_name='Имя для фильтра', max_length=50)
    unit = models.CharField(
        verbose_name='Единица измерения', max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.category.name} | {self.feature_name}'

    class Meta:
        verbose_name = 'Характеристики для товара'
        verbose_name_plural = 'Характеристики для товаров'
        unique_together = ('category', 'feature_name', 'feature_filter_name')


class FeatureValidator(models.Model):
    """
    Валидатор значений для конкретной характеристики,
    принадлежащей к конкретной категории
    """
    category = models.ForeignKey(
        'mainapp.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(
        CategoryFeature, verbose_name='Ключ характеристики',
        on_delete=models.CASCADE)
    # Для каждой категории и спец. характеристики для данной категории
    # присваиваем конкретное значение (уникальное)
    valid_feature_value = models.CharField(
        verbose_name='Валидное значение', max_length=100)

    def __str__(self):
        return (f'Категория "{self.category.name}" | '
                f'Характеристика "{self.feature_key.feature_name}" | '
                f'Валидное значение {self.valid_feature_value}')

    class Meta:
        verbose_name = 'Валидатор для спец. хар-к'
        verbose_name_plural = 'Валидаторы для спец. хар-к'


class ProductFeatures(models.Model):
    """Характеристики товара"""
    product = models.ForeignKey(
        'mainapp.Product', verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(
        CategoryFeature, verbose_name='Характеристика',
        on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=255)

    def __str__(self):
        return (f'Товар - "{self.product.title}" | '
                f'Характеристика - "{self.feature.feature_name}" | '
                f'Значение - {self.value}')

    class Meta:
        verbose_name = 'Характеристики товара'
        verbose_name_plural = 'Характеристики товаров'
