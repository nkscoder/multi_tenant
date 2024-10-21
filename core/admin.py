from django.contrib import admin
from django_tenants.utils import tenant_context
from django_tenants.admin import TenantAdminMixin
from .models import Tenant, Domain
from django.contrib.auth.admin import UserAdmin



from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Tenant, Domain,User

class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_on', 'paid_until', 'on_trial')
    # search_fields = ('name',)
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs  # Superusers can see all tenants
    #     return qs.filter(id=request.user.tenant.id)  # Filter for the current tenant

class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('tenant', 'is_primary')
    search_fields = ('domain',)
    # def get_queryset(self, request):
    #     """
    #     Restrict the queryset to domains belonging to the current tenant.
    #     Superusers can see all domains.
    #     """
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs  # Superusers can see all domains
    #     else:
    #         # Only return domains associated with the current tenant
    #         return qs.filter(tenant=request.tenant)

    # def has_change_permission(self, request, obj=None):
    #     """
    #     Ensure that an admin can only change the domain if it belongs to their tenant.
    #     Superusers can change all domains.
    #     """
    #     if not request.user.is_superuser and obj is not None:
    #         # Allow change only if the domain belongs to the current tenant
    #         return obj.tenant == request.tenant
    #     return super().has_change_permission(request, obj)

    # def save_model(self, request, obj, form, change):
    #     """
    #     Ensure that a domain is saved with the correct tenant.
    #     Prevent cross-tenant changes.
    #     """
    #     if not request.user.is_superuser:
    #         obj.tenant = request.tenant  # Ensure the domain is linked to the current tenant
    #     super().save_model(request, obj, form, change)




# class UserAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs  # Superusers can see all users
#         return qs.filter(tenant=request.tenant)  # Filter users for the current tenant

#     def has_change_permission(self, request, obj=None):
#         if obj is not None and not request.user.is_superuser:
#             return obj.tenant == request.tenant  # Allow change only if it belongs to the current tenant
#         return super().has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         if obj is not None and not request.user.is_superuser:
#             return obj.tenant == request.tenant  # Allow deletion only if it belongs to the current tenant
#         return super().has_delete_permission(request, obj)

class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all users
        return qs.filter(tenant=request.tenant)  # Filter users for the current tenant

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.tenant == request.tenant  # Allow change only if it belongs to the current tenant
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.tenant == request.tenant  # Allow deletion only if it belongs to the current tenant
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        # Ensure the tenant is set when saving the user
        if not request.user.is_superuser:
            obj.tenant = request.tenant  # Link to the current tenant
        # If the password has been changed, set it
        if form.cleaned_data['password']:  # Check if a new password is provided
            obj.set_password(form.cleaned_data['password'])  # Hash the new password

        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Domain, DomainAdmin)
