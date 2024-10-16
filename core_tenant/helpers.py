from .documents import get_index

def create_tenant_index(tenant):
    index = get_index(tenant)
    if not index.exists():
        index.create()  # Create Elasticsearch index for the tenant
