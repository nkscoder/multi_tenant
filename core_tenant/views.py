from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView
from .models import Product, Order
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.models import Tenant ,User # Import the Tenant model
from .services import search_products
from .utils import get_tenant_from_subdomain
from django.core.cache import cache  # Import the cache
from .services import search_products
from elasticsearch_dsl import Document, Text, Float, connections
conn =connections.create_connection(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "elastic"), 
    timeout=20
)

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Extract tenant schema name from the request's host
        host = request.get_host().split(':')[0]  # Remove port if present
        tenant_domain = host  # Assuming the domain is tenant-specific

        # Get the tenant based on the domain
        try:
            tenant = Tenant.objects.get(domains__domain=tenant_domain)
        except Tenant.DoesNotExist:
            messages.error(request, 'Invalid tenant domain.')
            return render(request, 'login.html')

        # Authenticate user by username, password, and tenant
        user = authenticate(request, username=username, password=password)

        if user is not None and user.tenant == tenant:
            login(request, user)  # Log the user in
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Redirect to a homepage or dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')  # Render the login form



def product_search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10  # Number of results per page

    # Get the tenant from the subdomain
    tenant = get_tenant_from_subdomain()

    if tenant:
        cache_key = f"search:{tenant}:{query}:{page}"
        results = cache.get(cache_key)

        # if results is None:  
        results = search_products(query, page, page_size)
        cache.set(cache_key, results, timeout=300)
        total_hits = results.hits.total.value
        total_pages = (total_hits + page_size - 1) // page_size  # Calculate total pages
        return render(request, 'product_search.html', {
            'results': results.hits,
            'query': query,
            'page': page,
            'total': total_hits,
            'page_size': page_size,
            'total_pages': total_pages,  # Pass total pages to template
        })
    else:
        return redirect('login')