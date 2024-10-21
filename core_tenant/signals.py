# # from django.db.models.signals import post_save
# # from django.dispatch import receiver
# # from .models import Product
# # from .documents import ProductDocument

# # @receiver(post_save, sender=Product)
# # def index_product(sender, instance, created, **kwargs):
# #     product_document = ProductDocument(
# #         meta={'id': instance.id},
# #         name=instance.name,
# #         description=instance.description,
# #         price=instance.price,
# #     )
# #     product_document.save()
# # from django.db.models.signals import post_save
# # from django.dispatch import receiver
# # from .models import Product
# # from .documents import ProductDocument

# # @receiver(post_save, sender=Product)
# # def index_product(sender, instance, created, **kwargs):
# #     # Create or update the document in Elasticsearch
# #     product_document = ProductDocument(
# #         meta={'id': instance.id},
# #         name=instance.name,
# #         description=instance.description,
# #         price=instance.price,
# #     )
# #     product_document.save()

# # from django.db.models.signals import post_save
# # from django.dispatch import receiver
# # from .models import Product
# # from .documents import ProductDocument

# # @receiver(post_save, sender=Product)
# # def index_product(sender, instance, created, **kwargs):
# #     product_document = ProductDocument(
# #         meta={'id': instance.id},  # Elasticsearch document ID
# #         name=instance.name,
# #         description=instance.description,
# #         price=instance.price,
# #     )
# #     product_document.save()  # Save the document to Elasticsearch
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Product
# from .documents import ProductDocument
# from .utils import get_tenant_from_subdomain  # Adjust the import as necessary

# import threading
# thread_locals = threading.local()

# # @receiver(post_save, sender=Product)
# # def index_product(sender, instance, created, **kwargs):
# #     request = getattr(thread_locals, 'request', None)  # Retrieve the request from thread-local storage

# #     if request:
# #         tenant = get_tenant_from_subdomain(request)


# #         # Dynamically set the index name based on the tenant ID
# #         ProductDocument.prepare(instance, tenant=tenant)

# #         # Prepare the document
# #         product_document = ProductDocument(
# #             meta={'id': instance.id},  # Elasticsearch document ID
# #             name=instance.name,
# #             description=instance.description,
# #             price=instance.price,
# #         )

# #         # Index the product in the correct Elasticsearch index
# #         product_document.save()


# # @receiver(post_save, sender=Product)
# # def index_product(sender, instance, created, **kwargs):
# #     # Retrieve the request from thread-local storage
# #     request = getattr(thread_locals, 'request', None)

# #     # Now you can use the request to get the tenant
# #     tenant = get_tenant_from_subdomain(request)
# #     tenant_string = tenant.schema_name if tenant else None

# #     # Prepare the document for Elasticsearch
# #     ProductDocument.prepare(instance, tenant=tenant_string)

# #     # Create and save the document to Elasticsearch
# #     product_document = ProductDocument(
# #         meta={'id': instance.id},  # Elasticsearch document ID
# #         name=instance.name,
# #         description=instance.description,
# #         price=instance.price,
# #     )
# #     product_document.save()  # Save the document to Elasticsearch



# # @receiver(post_save, sender=Product)
# # def index_product(sender, instance, created, **kwargs):
   
# #     # Index the product document
# #     if created:
# #         ProductDocument.prepare(instance)  # Prepare the document with tenant
# #         product_document = ProductDocument(
# #             meta={'id': instance.id},  # Set Elasticsearch document ID
# #             name=instance.name,
# #             description=instance.description,
# #             price=instance.price,
# #         )
# #         product_document.save()  #
# from crequest.middleware import CrequestMiddleware
# from core_tenant.models import Product
# from core.models import Tenant 
# @receiver(post_save, sender=Product)
# def index_product(sender, instance, created, **kwargs):
#     if created:
#         # Get the tenant dynamically from the request
#         request = CrequestMiddleware.get_request()
#         host = request.get_host().split('.')
#         subdomain = host[0]
        
#         # Ensure tenant is fetched based on the subdomain
#         try:
#             tenant = Tenant.objects.get(schema_name=subdomain)
#             # Set the tenant-specific index name
#             ProductDocument.Index.name = f"products_{tenant.id}"
#         except Tenant.DoesNotExist:
#             # Fallback to the base index name if no tenant is found
#             ProductDocument.Index.name = 'products'
        
#         # Create and save the document in Elasticsearch
#         product_document = ProductDocument(
#             meta={'id': instance.id},  # Set Elasticsearch document ID
#             name=instance.name,
#             description=instance.description,
#             price=instance.price,
#         )
#         product_document.save()  # This will automatically prepare and index the document


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .documents import ProductIndex

@receiver(post_save, sender=Product)
def index_product(sender, instance, **kwargs):
    product_index = ProductIndex(
        meta={'id': instance.id}, 
        name=instance.name, 
        description=instance.description, 
        price=float(instance.price)
    )
    product_index.save()  # This will create/update the index in Elasticsearch

@receiver(post_delete, sender=Product)
def delete_product_index(sender, instance, **kwargs):
    # Delete the product index from Elasticsearch when the product is deleted
    ProductIndex(meta={'id': instance.id}).delete()