from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.customer_accounts import models


class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = models.Workspace
        fields = ['name', 'description']


# class AddUserForm(UserCreationForm):
#     role = forms.CharField(max_length=50)

#     class Meta(UserCreationForm.Meta):
#         model = models.User
#         fields = ('username', 'role')


# class EditUserForm(UserChangeForm):
#     class Meta:
#         model = models.User
#         fields = ('username', 'email', 'first_name', 'last_name')


class TwoFactorForm(forms.Form):
    enable_2fa = forms.BooleanField(required=True)


class SessionTimeoutForm(forms.Form):
    timeout_duration = forms.IntegerField(min_value=1)


class SSOForm(forms.Form):
    enable_sso = forms.BooleanField(required=True)


class WorkspaceInvitationForm(forms.Form):
    email = forms.EmailField()
    role = forms.CharField(max_length=50)


