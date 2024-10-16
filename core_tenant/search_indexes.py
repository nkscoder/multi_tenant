from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl.connections import connections
from .models import Product
from core.models import  Tenant
# Connect to the Elasticsearch server
connections.create_connection()

# Define index name
def tenant_index_name(tenant):
    return f"{tenant.schema_name}_products"

# Create an Elasticsearch index for each tenant
def get_index(tenant):
    return Index(tenant_index_name(tenant))

# Define a document to index tenant-specific data
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
            index.save(self)
        else:
            super().save(*args, **kwargs)
