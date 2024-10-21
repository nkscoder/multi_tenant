from django.utils.deprecation import MiddlewareMixin

from .models import Tenant

# class TenantMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         domain = request.META.get('HTTP_HOST', '')
#         tenant = Tenant.objects.filter(domain=domain).first()
#         if tenant:
#             request.tenant = tenant
#         else:
#             request.tenant = None  # Handle invalid tenant appropriately

#         response = self.get_response(request)
#         return response
    
    
# class TenantMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Extract tenant from subdomain
#         host = request.get_host().split(':')[0]  # Get host without port
#         subdomain = host.split('.')[0]  # Assuming subdomain is the first part (tenant1, tenant2, etc.)
        
#         try:
#             # import ipdb; ipdb.set_trace()
#             tenant = Tenant.objects.get(schema_name=subdomain)
#             request.tenant = tenant  # Attach tenant to the request
#         except Tenant.DoesNotExist:
#             # import ipdb; ipdb.set_trace()
#             request.tenant = None
import threading

# Create a thread-local storage instance
thread_locals = threading.local()
class ThreadLocalMiddleware:
    """Middleware to store the request in thread-local storage."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_locals.request = request  # Store the request
        response = self.get_response(request)  # Process the request
        return response
