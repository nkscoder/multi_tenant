from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Order
from .documents import get_index

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'


def search_products(tenant, query):
    index = get_index(tenant)
    search = index.search().query("match", name=query)
    return search.execute()
