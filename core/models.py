from django.db import models
from django_tenants.models import TenantMixin,DomainMixin
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token as DefaultToken
from django.conf import settings

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


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)
    
    
class User(AbstractUser):
    objects = UserManager()

    tenant = models.ForeignKey(
        'Tenant', 
        on_delete=models.CASCADE,
        related_name='users'
    )

    groups = models.ManyToManyField(
        Group,
        related_name='core_user_groups',  # Use a unique related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='core_user_permissions',  # Use a unique related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        unique_together = ('username', 'tenant')  # Ensure usernames are unique per tenant
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} ({self.tenant})'
    
    
    

# class Token(DefaultToken):
#     custom_user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         related_name='auth_tokens', 
#         on_delete=models.CASCADE
#     )    