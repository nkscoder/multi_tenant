from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl.connections import connections
from .models import Product
from core.models import Tenant

# Connect to the Elasticsearch server
connections.create_connection()

# Define index name based on tenant schema
def tenant_index_name(tenant):
    return f"{tenant.schema_name}_products"

# Create an Elasticsearch index for each tenant
def get_index(tenant):
    index = Index(tenant_index_name(tenant))
    index.settings(
        number_of_shards=1,
        number_of_replicas=0,
    )
    return index

# Define a document for indexing tenant-specific product data
class ProductDocument(Document):
    name = fields.TextField()
    description = fields.TextField()
    price = fields.FloatField()

    class Django:
        model = Product

    def save(self, *args, **kwargs):
        tenant = kwargs.pop('tenant', None)
        if tenant:
            index = get_index(tenant)
            if not index.exists():
                index.create()  # Create index if it doesn't exist
            index.save(self)  # Save document to the tenant-specific index
        else:
            super().save(*args, **kwargs)
