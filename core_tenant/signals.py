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