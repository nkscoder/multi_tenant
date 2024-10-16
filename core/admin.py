from django.contrib import admin
from django_tenants.utils import tenant_context
from django_tenants.admin import TenantAdminMixin
from .models import Tenant, Domain
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Tenant, Domain

class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_on', 'paid_until', 'on_trial')
    search_fields = ('name',)

class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('tenant', 'is_primary')
    search_fields = ('domain',)

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Domain, DomainAdmin)
