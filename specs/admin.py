from django.contrib import admin

from .models import CategoryFeature, FeatureValidator, ProductFeatures

admin.site.register(CategoryFeature)
admin.site.register(FeatureValidator)
admin.site.register(ProductFeatures)
