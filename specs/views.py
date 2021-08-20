from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .forms import NewCategoryForm, NewCateoryFeatureKeyForm


class BaseSpecView(View):
    """Админка характеристик"""

    def get(self, request, *args, **kwargs):
        return render(request, 'specs/product_features.html', {})


class NewCategoryView(View):
    """Создать новую категорию"""

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'specs/new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/product-specs/')
        context = {'form': form}
        return render(request, 'specs/new_category.html', context)


class CreateNewFeature(View):
    """Создать новую характеристику"""

    def get(self, request, *args, **kwargs):
        form = NewCateoryFeatureKeyForm(request.POST or None)
        context = {'form': form}
        return render(request, 'specs/new_feature.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCateoryFeatureKeyForm(request.POST or None)
        if form.is_valid():
            new_category_feature_key = form.save(commit=False)
            new_category_feature_key.category = form.cleaned_data['category']
            new_category_feature_key.feature_name = form.cleaned_data['feature_name']
            new_category_feature_key.save()
            return HttpResponseRedirect('/product-specs/')
        context = {'form': form}
        return render(request, 'specs/new_feature.html', context)
