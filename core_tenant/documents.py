from elasticsearch_dsl import Document, Text, Float, connections
from django_tenants.utils import tenant_context
from .utils import get_tenant_from_subdomain



conn =connections.create_connection(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "elastic"), 
    timeout=20
)

class ProductIndex(Document):
    name = Text()         # This allows full-text search
    description = Text()  # This allows full-text search
    price = Float()       # Store price as a float

    class Index:
        name = "product_index"  # Placeholder name; will be set dynamically

    def save(self, *args, **kwargs):
        # Set index name dynamically based on the tenant schema
        self._index = f"product_{self.get_current_tenant_schema_name()}_index"
        
        # Ensure the index exists before saving
        if not self.index_exists():
            print(f"Index {self._index} does not exist, creating it.")
            self.create_index()  # Create the index if it doesn't exist
        else:
            print(f"Index {self._index} exists.")
        self.meta.index = self._index
        
        # Log the index where you are saving the document
        print(f"Saving document to index: {self._index}")
        
        # Now call super to save the document
        
        try:
            super(ProductIndex, self).save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving document: {e}")

    def index_exists(self):
        """Check if the index exists."""
        return conn.indices.exists(index=self._index)

    def create_index(self):
        """Create the index with the required mappings."""
        # Define the settings and mappings for the index
        index_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "description": {"type": "text"},
                    "price": {"type": "float"}
                }
            }
        }

        try:
            # Create the index if it doesn't exist
            if not self.index_exists():
                conn.indices.create(index=self._index, body=index_body)
        except Exception as e:  # Catch all exceptions
            print(f"Error creating index: {e}")  # Log or handle the error

    def get_current_tenant_schema_name(self):
        """Return the schema name of the current tenant."""
        return self.get_tenant_schema_name()

    @classmethod
    def get_tenant_schema_name(cls):
        """Get the tenant schema name from your multi-tenant middleware."""
        tenant = get_tenant_from_subdomain()  # Modify based on your actual tenant fetching logic
        return tenant.schema_name
