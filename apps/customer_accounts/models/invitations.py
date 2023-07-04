import datetime


from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _l
from django.utils import timezone
from django.utils.crypto import get_random_string

from django_multitenant.models import TenantModel
from invitations.base_invitation import AbstractBaseInvitation
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings
from invitations import signals

User = settings.AUTH_USER_MODEL


class CustomInvitation(TenantModel, AbstractBaseInvitation):
    '''
    adding three extra fields to Invitation model
    '''
    tenant_id = 'account_id'
    email = models.EmailField(
        unique=True,
        verbose_name=_l("e-mail address"),
        max_length=app_settings.EMAIL_MAX_LENGTH,
    )
    created = models.DateTimeField(verbose_name=_l("created"), default=timezone.now)

    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='invitations', null=True, blank=True)
    workspace = models.ForeignKey('Workspace', on_delete=models.CASCADE, related_name='invitations', null=True, blank=True)
    account = models.ForeignKey('CustomerAccount', on_delete=models.CASCADE, related_name='invitations', null=True, blank=True)

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email, key=key, inviter=inviter, **kwargs
        )
        return instance

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY,
        )
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = get_current_site(request)
        invite_url = reverse(app_settings.CONFIRMATION_URL_NAME, args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update(
            {
                "invite_url": invite_url,
                "site_name": current_site.name,
                "email": self.email,
                "key": self.key,
                "inviter": self.inviter,
            },
        )

        email_template = "invitations/email/email_invite"

        get_invitations_adapter().send_mail(email_template, self.email, ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter,
        )

    def __str__(self):
        return f"Invite: {self.email}"
