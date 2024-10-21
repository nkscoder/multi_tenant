# utils.py
from crequest.middleware import CrequestMiddleware

from core.models import Tenant  # Adjust the import to your Tenant model


def get_tenant_from_subdomain():
    """
    Retrieve the tenant from the subdomain of the request.
    Assumes the subdomain is the schema name of the tenant.
    """
    request  = CrequestMiddleware.get_request()
 # Get the current request
    if not request:
        return None  # Or handle accordingly

    host = request.get_host().split('.')
    subdomain = host[0]  # Get the first part of the domain as the subdomain

    try:
        return Tenant.objects.get(schema_name=subdomain)  # Assuming you have a schema_name field in your Tenant model
    except Tenant.DoesNotExist:
        return None