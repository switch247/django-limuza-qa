from django.conf import settings
from django.db import models

from django_extensions.db.fields import AutoSlugField
from django_multitenant.fields import TenantForeignKey
from django_multitenant.models import TenantModel


User = settings.AUTH_USER_MODEL


class SubscriptionPlanManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


# maybe worth adding currency in the future?
class SubscriptionPlan(models.Model):
    objects = SubscriptionPlanManager()
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.slug,


class SubscriptionManager(models.Manager):
    def get_by_natural_key(self, subscription_plan_slug, account_slug):
        return self.get(subscription_plan_slug=subscription_plan_slug, account_slug=account_slug)


class Subscription(TenantModel):
    objects = SubscriptionManager()
    tenant_id = 'account_id'
    account = models.ForeignKey('CustomerAccount', on_delete=models.CASCADE, related_name='subscriptions')
    # todo maybe subscribtion code?? reference
    subscription_plan = TenantForeignKey(SubscriptionPlan, on_delete=models.CASCADE, null=False, blank=False)
    subscription_start = models.DateTimeField(auto_now_add=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tenant_id} - {self.subscription_plan.name}'

    def natural_key(self):
        return self.subscription_plan.slug, self.account.slug


class CustomerAccountTenantManager(models.Manager):
    require_filter_tenant = True

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class CustomerAccount(TenantModel):
    tenant_id = 'id'
    objects = CustomerAccountTenantManager()
    all_tenants = models.Manager()

    name = models.CharField(max_length=200, null=False, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True, null=False, blank=False, overwrite=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # todo add update this field on save()
    is_active = models.BooleanField(default=True)

    class Meta:
        base_manager_name = 'all_tenants'

    class TenantMeta:
        tenant_field_name = 'id'

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.slug,


class TenantClass(TenantModel):
    account = TenantForeignKey(CustomerAccount, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    class TenantMeta:
        tenant_field_name = 'account_id'


class WorkspaceManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Workspace(TenantModel):
    objects = WorkspaceManager()
    tenant_id = 'account_id'
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True, null=False, blank=False)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, related_name='workspaces')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # add update this field on save()

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.slug,
