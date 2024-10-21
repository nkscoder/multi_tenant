from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView
from .models import Product, Order
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.models import Tenant ,User # Import the Tenant model

# from .documents import get_index
from .services import search_products
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



# def product_search(request):
#     query = request.GET.get('q', '')
#     page = int(request.GET.get('page', 1))
#     page_size = 10  # Number of results per page
#     if request.user.is_authenticated:
#         tenant = request.user.tenant  # Get the tenant for authenticated users
#         results = search_products(query, page, page_size, tenant)
#     else:
#         # Redirect to login page or show a message
#         return redirect('login') 
#     return render(request, 'product_search.html', {
#         'results': results,
#         'query': query,
#         'page': page,
#         'total': results.hits.total.value,
#         'page_size': page_size,
#     })

from django.shortcuts import render, redirect
from .services import search_products,create_index_if_not_exists
from .utils import get_tenant_from_subdomain
from django.core.cache import cache  # Import the cache

  # Ensure this function retrieves the tenant

# def product_search(request):
#     query = request.GET.get('q', '')
#     page = int(request.GET.get('page', 1))
#     page_size = 10  # Number of results per page

#     # Get the tenant from the request (set by middleware)
#     # Get the tenant from the subdomain
#     tenant = get_tenant_from_subdomain(request)

#     if tenant:
#         results = search_products(query, page, page_size, tenant)
#     else:
#         return redirect('login')
        
#     if tenant:
#         results = search_products(query, page, page_size, tenant)
#     else:
#         return redirect('login')  # Or handle missing tenant error here

#     return render(request, 'product_search.html', {
#         'results': results,
#         'query': query,
#         'page': page,
#         'total': results.hits.total.value,
#         'page_size': page_size,
#     })

from elasticsearch_dsl.connections import connections

# Ensure connection is initialized
connections.create_connection(alias='default', hosts=['http://localhost:9200'])

# def product_search(request):
#     query = request.GET.get('q', '')
#     page = int(request.GET.get('page', 1))
#     page_size = 10  # Number of results per page

#     # Get the tenant from the subdomain
#     tenant = get_tenant_from_subdomain()

#     # Generate a cache key based on query, page, and tenant
#     cache_key = f"search:{tenant}:{query}:{page}"

#     # Check if the search results are already cached
#     results = cache.get(cache_key)

#     if results is None:  # If not cached, perform the search and cache the results
#         if tenant:
#             results = search_products(query, page, page_size, tenant)
#         else:
#             return redirect('login')

#         # Cache the results for future use (set cache timeout as needed, e.g., 300 seconds)
#         cache.set(cache_key, results, timeout=300)

#     return render(request, 'product_search.html', {
#         'results': results,
#         'query': query,
#         'page': page,
#         'total': results.hits.total.value,
#         'page_size': page_size,
#     })


def product_search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10  # Number of results per page

    # Get the tenant from the subdomain
    tenant = get_tenant_from_subdomain()

    if tenant:
        index_name = f"products_{tenant.id}"
        create_index_if_not_exists(index_name)  # Ensure index exists

        # Generate a cache key based on query, page, and tenant
        cache_key = f"search:{tenant}:{query}:{page}"

        # Check if the search results are already cached
        results = cache.get(cache_key)

        if results is None:  # If not cached, perform the search and cache the results
            results = search_products(query, page, page_size, tenant)

            # Cache the results for future use (set cache timeout as needed, e.g., 300 seconds)
            cache.set(cache_key, results, timeout=300)

        return render(request, 'product_search.html', {
            'results': results,
            'query': query,
            'page': page,
            'total': results.hits.total.value,
            'page_size': page_size,
        })
    else:
        return redirect('login')
