from django.db import models
from django_tenants.models import TenantMixin,DomainMixin

# Tenant Model
class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # Define any other fields that should be global to all tenants

    def __str__(self):
        return self.name

# Domain Model
class Domain(DomainMixin):
    pass