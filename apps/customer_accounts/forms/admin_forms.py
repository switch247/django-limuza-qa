from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _l

from invitations.forms import CleanEmailMixin
from invitations.utils import get_invitation_model
from apps.customer_accounts import models

User = get_user_model()
Invitation = get_invitation_model()


class CustomInvitationAdminAddForm(forms.ModelForm, CleanEmailMixin):
    email = forms.EmailField(
        label=_l("Email"),
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"}),
    )
    inviter = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name="id")
    role = forms.ModelChoiceField(queryset=models.Role.objects.all(), to_field_name="id")
    workspace = forms.ModelChoiceField(queryset=models.Workspace.objects.all(), to_field_name="id")
    account = forms.ModelChoiceField(queryset=models.CustomerAccount.objects.all(), to_field_name="id")

    def save(self, *args, **kwargs):
        cleaned_data = super().clean()
        instance = Invitation.create(**cleaned_data)
        instance.send_invitation(self.request)
        super().save(*args, **kwargs)
        return instance

    class Meta:
        model = Invitation
        fields = ('email', 'inviter', 'role', 'workspace', 'account')
