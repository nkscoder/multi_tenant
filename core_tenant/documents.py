

# # from django_elasticsearch_dsl import Document, fields, Index
# # from .models import Product

# # # Define an Elasticsearch index
# # products_index = Index('products')

# # # Configure the index settings
# # products_index.settings(
# #     number_of_shards=1,
# #     number_of_replicas=0,
# # )

# # @products_index.document
# # class ProductDocument(Document):
# #     name = fields.TextField()
# #     description = fields.TextField()
# #     price = fields.FloatField()

# #     class Django:
# #         model = Product

# # from django_elasticsearch_dsl import Document, fields, Index
# # from .models import Product
# # from elasticsearch_dsl.connections import connections

# # # Ensure connection is initialized
# # connections.create_connection(alias='default', hosts=['http://localhost:9200'])
# # # Define an Elasticsearch index
# # products_index = Index('products')

# # # Configure the index settings
# # products_index.settings(
# #     number_of_shards=1,
# #     number_of_replicas=0,
# # )

# # @products_index.document
# # class ProductDocument(Document):
# #     name = fields.TextField()
# #     description = fields.TextField()
# #     price = fields.FloatField()

# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',  # Include the ID field if you want to reference it in Elasticsearch
# #         ]

# #         # Optionally, if you want to customize the behavior further, you can add:
# #         # def get_queryset(self):
# #         #     return super().get_queryset().filter(active=True)  # Example of filtering

# # # Ensure the index exists
# # if not products_index.exists():
# #     products_index.create()



# # from django_elasticsearch_dsl import Document
# # from django_elasticsearch_dsl.registries import registry
# # from .models import Product
# # from elasticsearch_dsl.connections import connections
# # connections.create_connection(alias='default', hosts=['http://localhost:9200'])


# # @registry.register_document
# # class ProductDocument(Document):
# #     class Index:
# #         # Name of the Elasticsearch index
# #         name = 'products'
    
# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',
# #             'name',
# #             'description',
# #             'price',
# #         ]


# # from django_elasticsearch_dsl import Document
# # from django_elasticsearch_dsl.registries import registry
# # from .models import Product
# # from elasticsearch_dsl.connections import connections

# # # Establishing connection to Elasticsearch
# # connections.create_connection(alias='default', hosts=['http://localhost:9200'])

# # @registry.register_document
# # class ProductDocument(Document):
# #     class Index:
# #         # Define the base name of the Elasticsearch index
# #         name = 'products'  # Base index name, will be modified with tenant info

# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',
# #             'name',
# #             'description',
# #             'price',
# #         ]

# #     def get_index_name(self):
# #         # Return the index name based on the tenant
# #         tenant_id = self.instance.tenant.id  # Assuming `tenant` is a ForeignKey in your Product model
# #         return f"{self.Index.name}_{tenant_id}"  # Use tenant ID to create a unique index name

# #     @classmethod
# #     def prepare(cls, instance):
# #         # Prepare method to include the tenant in the indexing process
# #         cls.Index.name = f"{cls.Index.name}_{instance.tenant.id}"  # Dynamically set index name based on tenant

# #         # Call the parent prepare method
# #         return super().prepare(instance)

# #     @classmethod
# #     def get_queryset(cls):
# #         # Override the queryset method to ensure we fetch the correct tenant's products
# #         return super().get_queryset().filter(tenant=cls.tenant)

# #     @classmethod
# #     def update(cls, instance, **kwargs):
# #         # Custom update logic to ensure tenant's index is used
# #         cls.prepare(instance)
# #         super().update(instance, **kwargs)


# # from django_elasticsearch_dsl import Document
# # from django_elasticsearch_dsl.registries import registry
# # from .models import Product
# # from elasticsearch_dsl.connections import connections

# # # Establishing connection to Elasticsearch
# # connections.create_connection(alias='default', hosts=['http://localhost:9200'])

# # @registry.register_document
# # class ProductDocument(Document):
# #     class Index:
# #         name = 'products'  # Base index name, will be modified with tenant info

# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',
# #             'name',
# #             'description',
# #             'price',
# #         ]

# #     @classmethod
# #     def prepare(cls, instance, tenant=None):
# #         if tenant:
# #             # Set index name based on tenant string
# #             cls.Index.name = f"{cls.Index.name}_{tenant}"  # Use tenant string directly
# #         else:
# #             cls.Index.name = cls.Index.name  # Fallback to base index name if tenant is not found

# #         # Call the parent prepare method
# #         return super().prepare(instance)

# #     @classmethod
# #     def get_queryset(cls):
# #         # Override the queryset method if needed to filter products by tenant
# #         return super().get_queryset()  # Adjust if your models support tenant filtering

# #     @classmethod
# #     def update(cls, instance, tenant=None, **kwargs):
# #         # Custom update logic to ensure tenant's index is used
# #         cls.prepare(instance, tenant)
# #         super().update(instance, **kwargs)


# # from django_elasticsearch_dsl import Document
# # from django_elasticsearch_dsl.registries import registry
# # from .models import Product
# # from elasticsearch_dsl.connections import connections

# # # Establishing connection to Elasticsearch
# # connections.create_connection(alias='default', hosts=['http://localhost:9200'])

# # @registry.register_document
# # class ProductDocument(Document):
# #     class Index:
# #         name = 'products'  # Base index name, will be modified with tenant info

# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',
# #             'name',
# #             'description',
# #             'price',
# #         ]

# #     @classmethod
# #     def prepare(cls, instance, tenant=None):
# #         if tenant:
# #             # Set index name based on tenant string
# #             cls.Index.name = f"{cls.Index.name}_{tenant.id}"  # Use tenant string directly
# #         else:
# #             cls.Index.name = cls.Index.name  # Fallback to base index name if tenant is not found

# #         # Call the parent prepare method with the instance
# #         return super().prepare(instance)

# #     @classmethod
# #     def get_queryset(cls):
# #         # Override the queryset method if needed to filter products by tenant
# #         return super().get_queryset()  # Adjust if your models support tenant filtering

# #     @classmethod
# #     def update(cls, instance, tenant=None, **kwargs):
# #         # Custom update logic to ensure tenant's index is used
# #         import ipdb; ipdb.set_trace()
# #         cls.prepare(instance, tenant)
# #         super().update(instance, **kwargs)

# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from .models import Product
# from .utils import *
# from elasticsearch_dsl.connections import connections
# import threading
# thread_locals = threading.local()
# from crequest.middleware import CrequestMiddleware

# from core.models import Tenant 
# # Establishing connection to Elasticsearch
# connections.create_connection(alias='default', hosts=['http://localhost:9200'])

# # @registry.register_document
# # class ProductDocument(Document):
# #     class Index:
# #         name = 'products'  # Base index name, will be modified with tenant info

# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',
# #             'name',
# #             'description',
# #             'price',
# #         ]

# #     @classmethod
# #     def prepare(cls, instance, tenant=None):
# #         if tenant is None:
# #             request  = CrequestMiddleware.get_request()
# #             host = request.get_host().split('.')
# #             subdomain = host[0]  
# #             tenant= Tenant.objects.get(schema_name=subdomain) 
# #         # Set the index name based on the tenant string or fallback to the base name
# #         if tenant:
# #             cls.Index.name = f"{cls.Index.name}_{tenant.id}"  # Use tenant ID directly
# #         else:
# #             cls.Index.name = cls.Index.name  # Fallback to base index name if tenant is not found

# #         # Call the parent prepare method with the instance
# #         return super().prepare(instance)

# #     @classmethod
# #     def get_queryset(cls):
# #         # You may want to filter by tenant here if necessary
# #         return super().get_queryset()  # Adjust if your models support tenant filtering

# #     @classmethod
# #     def update(cls, instance, tenant=None, **kwargs):
# #         request  = CrequestMiddleware.get_request()
# #         host = request.get_host().split('.')
# #         subdomain = host[0]  
# #         tenant= Tenant.objects.get(schema_name=subdomain)  # Assuming you have a schema_name field in your Tenant model
# #         cls.prepare(instance, tenant)  # Prepare with the tenant object
# #         super().update(instance, **kwargs)  # Update the document


# # @registry.register_document
# # class ProductDocument(Document):
# #     class Index:
# #         name = 'products'  # Base index name, will be modified with tenant info

# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',
# #             'name',
# #             'description',
# #             'price',
# #         ]

# #     @classmethod
# #     def prepare(cls, instance):
# #         """
# #         Prepare the document for indexing by dynamically setting the index name
# #         based on the tenant retrieved from the request's subdomain.
# #         """
# #         # Get the tenant dynamically from the request
# #         request = CrequestMiddleware.get_request()
# #         host = request.get_host().split('.')
# #         subdomain = host[0]  
        
# #         # Ensure tenant is fetched based on the subdomain
# #         try:
# #             tenant = Tenant.objects.get(schema_name=subdomain)
# #             # Set the index name based on the tenant
# #             cls.Index.name = f"products_{tenant.id}"
# #         except Tenant.DoesNotExist:
# #             # Fallback to the base index name if no tenant is found
# #             cls.Index.name = 'products'

# #         # Call the parent prepare method to prepare the instance for indexing
# #         return super().prepare(instance)

# #     @classmethod
# #     def get_queryset(cls):
# #         """
# #         Optionally, filter the queryset based on the tenant or other criteria.
# #         """
# #         # Here you can filter the queryset for the current tenant, if necessary
# #         return super().get_queryset()

# #     @classmethod
# #     def update(cls, instance, **kwargs):
# #         """
# #         Update the document in Elasticsearch. Prepares the document using the tenant info
# #         and then updates the instance in Elasticsearch.
# #         """
# #         # Prepare the document before updating
# #         cls.prepare(instance)
# #         # Call the parent update method to update the document in Elasticsearch
# #         super().update(instance, **kwargs)


# # @registry.register_document
# # class ProductDocument(Document):
# #     class Index:
# #         name = 'products'  # Base index name, will be modified with tenant info

# #     class Django:
# #         model = Product  # The model associated with this Document
# #         fields = [
# #             'id',
# #             'name',
# #             'description',
# #             'price',
# #         ]

# #     @classmethod
# #     def get_queryset(cls):
# #         """
# #         Optionally, filter the queryset based on the tenant or other criteria.
# #         """
# #         # Here you can filter the queryset for the current tenant, if necessary
# #         return super().get_queryset()

# #     # @classmethod
# #     # def update(cls, instance, **kwargs):
# #     #     """
# #     #     Update the document in Elasticsearch. Prepares the document using the tenant info
# #     #     and then updates the instance in Elasticsearch.
# #     #     """
# #     #     # Get the tenant dynamically from the request
# #     #     request = CrequestMiddleware.get_request()
# #     #     host = request.get_host().split('.')
# #     #     subdomain = host[0]
        
# #     #     # Ensure tenant is fetched based on the subdomain
# #     #     try:
# #     #         tenant = Tenant.objects.get(schema_name=subdomain)
# #     #         # Set the tenant-specific index name
# #     #         cls.Index.name = f"products_{tenant.id}"
# #     #     except Tenant.DoesNotExist:
# #     #         # Fallback to the base index name if no tenant is found
# #     #         cls.Index.name = 'products'
        
# #     #     # Call the parent update method to update the document in Elasticsearch
# #     #     super().update(instance, **kwargs)
# #     @classmethod
# #     def update(cls, instance, **kwargs):
# #         """
# #         Update the document in Elasticsearch. Prepares the document using the tenant info
# #         and then updates the instance in Elasticsearch.
# #         """
# #         # Get the tenant dynamically from the request
# #         request = CrequestMiddleware.get_request()
# #         host = request.get_host().split('.')
# #         subdomain = host[0]
        
# #         # Ensure tenant is fetched based on the subdomain
# #         try:
# #             tenant = Tenant.objects.get(schema_name=subdomain)
# #             # Set the tenant-specific index name
# #             cls.Index.name = f"products_{tenant.id}"
# #         except Tenant.DoesNotExist:
# #             # Fallback to the base index name if no tenant is found
# #             cls.Index.name = 'products'
        
# #         # Call the parent update method, passing the instance
# #         super(ProductDocument, cls).update(instance, **kwargs)

# @registry.register_document
# class ProductDocument(Document):
#     class Index:
#         name = 'products'  # Base index name, will be modified with tenant info

#     class Django:
#         model = Product  # The model associated with this Document
#         fields = [
#             'id',
#             'name',
#             'description',
#             'price',
#         ]

#     @classmethod
#     def get_queryset(cls):
#         """
#         Optionally, filter the queryset based on the tenant or other criteria.
#         """
#         return super().get_queryset()

#     @classmethod
#     def update(cls, instance, **kwargs):
#         """
#         Update the document in Elasticsearch. Prepares the document using the tenant info
#         and then updates the instance in Elasticsearch.
#         """
#         # Get the tenant dynamically from the request
#         request = CrequestMiddleware.get_request()
#         host = request.get_host().split('.')
#         subdomain = host[0]
        
#         # Ensure tenant is fetched based on the subdomain
#         try:
#             tenant = Tenant.objects.get(schema_name=subdomain)
#             # Set the tenant-specific index name
#             cls.Index.name = f"products_{tenant.id}"
#         except Tenant.DoesNotExist:
#             # Fallback to the base index name if no tenant is found
#             cls.Index.name = 'products'
        
#         # Call the parent update method, passing the instance explicitly
#         super(ProductDocument, cls).update(instance, **kwargs)  # Pass the `instance` here


# from elasticsearch_dsl import Document, Text, Keyword, Float, connections
# from django_tenants.utils import get_current_tenant

# # Create an Elasticsearch connection
# connections.create_connection(hosts=['localhost'], timeout=20)

# class ProductIndex(Document):
#     name = Text()         # This allows full-text search
#     description = Text()  # This allows full-text search
#     price = Float()       # Store price as a float

#     class Index:
#         # Use a function to generate tenant-specific index name
#         name = f"product_{get_current_tenant().schema_name}_index"  # Dynamic index name

#     def save(self, *args, **kwargs):
#         # Any custom logic before saving can go here
#         super().save(*args, **kwargs)

# core_tenant/documents.py

from elasticsearch_dsl import Document, Text, Float, connections
from django_tenants.utils import tenant_context
from django.conf import settings

# Create an Elasticsearch connection
connections.create_connection(hosts=['http://localhost:9200'], timeout=20)

class ProductIndex(Document):
    name = Text()         # This allows full-text search
    description = Text()  # This allows full-text search
    price = Float()       # Store price as a float

    class Index:
        name = "product_index"  # Placeholder name; will be set dynamically

    def save(self, *args, **kwargs):
        # Set index name dynamically based on the tenant
        self._index = f"product_{self.get_current_tenant_schema_name()}_index"
        super().save(*args, **kwargs)

    def get_current_tenant_schema_name(self):
        # Return the schema name of the current tenant
        return self.get_tenant_schema_name()

    @classmethod
    def get_tenant_schema_name(cls):
        # Get the tenant schema name; you may need to adjust this according to your middleware setup
        from django_tenants.utils import get_tenant_model
        request = cls.get_request()
        tenant = request.tenant
        return tenant.schema_name

    @classmethod
    def get_request(cls):
        from threading import local
        return local().request

