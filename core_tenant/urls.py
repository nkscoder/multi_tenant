from django.urls import path
from .views import ProductListView, OrderDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
