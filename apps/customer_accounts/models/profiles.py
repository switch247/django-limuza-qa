from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_extensions.db.fields import AutoSlugField
from django_multitenant.models import TenantModel

from apps.customer_accounts import models as accounts_models

User = settings.AUTH_USER_MODEL


class RoleManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Role(models.Model):
    objects = RoleManager()
    nice_name = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True, null=False, blank=False)

    def __str__(self):
        return self.nice_name

    def natural_key(self):
        return (self.slug,)


class ProfileManager(models.Manager):
    def get_by_natural_key(self, email):
        return self.get(user__email=email)


class Profile(TenantModel):
    objects = ProfileManager()
    tenant_id = 'account_id'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=False, blank=False)
    account = models.ForeignKey('CustomerAccount', on_delete=models.PROTECT, related_name='profiles')
    workspace = models.ManyToManyField('Workspace', related_name='profiles')

    def __str__(self):
        return f'{self.user.email} - {self.role.nice_name}'

    def natural_key(self):
        return (self.user.email,)

    @property
    def invitation(self):
        '''Returns invitation or None'''
        return accounts_models.CustomInvitation.objects.filter(email=self.user.email).first()


def create_profile_from_invite(instance, created, **kwargs):

    invitation = accounts_models.CustomInvitation.objects.filter(email=instance.email).first()
    if invitation:
        profile = Profile.objects.create(
            user=instance,
            role=invitation.role,
            account=invitation.account,
        )
        profile.save()
        profile.workspace.set(invitation.workspace)
        profile.save()


def create_profile_with_basic_account(instance, created, **kwargs):
    customer_account = accounts_models.CustomerAccount.objects.create(
        name=instance.username,
        is_active=False,  # initial creation is inactive
    )
    subscription_plan = accounts_models.SubscriptionPlan.objects.filter(name='Basic').first()
    if not subscription_plan:
        subscription_plan = accounts_models.SubscriptionPlan.objects.create(
            name='Basic',
            price=1000,
        )
    accounts_models.Subscription.objects.create(
        subscription_plan=subscription_plan,
        account=customer_account,
    )
    profile = Profile.objects.create(
        account_id=customer_account.id,
        user=instance,
        role=Role.objects.filter(name='account_owner').first(),
        account=customer_account,
    )
    profile.save()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    This signal ensures that any user created gets a profile
    """
    if not accounts_models.Role.objects.all().exists():
        raise Exception('No roles have been created. Please run the management command initial_setup')
    if created and accounts_models.CustomInvitation.objects.filter(email=instance.email).exists():
        create_profile_from_invite(instance, created, **kwargs)

    if created:
        create_profile_with_basic_account(instance, created, **kwargs)