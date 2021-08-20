from django.urls import path

from .api_views import CategoryAPIView, CustomersListAPIView

urlpatterns = [
    path('categories/<str:id>/', CategoryAPIView.as_view(),
         name='category_list'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list'),
]
