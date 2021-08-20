from django.urls import path

from .views import BaseSpecView, NewCategoryView, CreateNewFeature

urlpatterns = [
    path('new-feature/', CreateNewFeature.as_view(), name='new-feature'),
    path('new-category/', NewCategoryView.as_view(), name='new-category'),
    path('', BaseSpecView.as_view(), name='base-specs'),
]
