from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('search/', product_search, name='product_search'),
    path('', product_search, name='search'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),



]

