from django.contrib.auth import get_user_model
from django.urls import reverse

from allauth.account.models import EmailAddress
import pytest

from apps.customer_accounts import models
from apps.customer_accounts.tests.fixtures import *  # noqa

User = get_user_model()

# test save method on profile

# test adding workspaces to user profile

# user has only one workspace???
USER_DATA = {
    'username': 'testuser',
    'email': 'first_user@here.com',
    'password1': 'testpassword',
    'password2': 'testpassword',
}


@pytest.mark.django_db
def test_create_user(client, load_initial_data):
    assert models.Role.objects.all().exists
    users_initial_count = User.objects.count()
    email_initial_count = EmailAddress.objects.count()
    response = client.post(reverse('account_signup'), USER_DATA)
    assert response.status_code == 302
    assert User.objects.count() == users_initial_count + 1
    assert EmailAddress.objects.count() == email_initial_count + 1


@pytest.mark.django_db
def test_create_profile_save_method(client, load_initial_data):
    profiles_initial_count = models.Profile.objects.count()
    response = client.post(reverse('account_signup'), USER_DATA)
    assert response.status_code == 302
    assert models.Profile.objects.count() == profiles_initial_count + 1
    profile = models.Profile.objects.filter(user__email=USER_DATA['email']).first()
    assert profile is not None
    assert profile.account.name == 'first_user'
    # there can be more than one subscription
    subscription = profile.account.subscriptions.first()
    assert subscription.subscription_plan.name == 'Basic'
    assert profile.role.name == 'account_owner'

@pytest.mark.django_db
def test_create_and_upgrade_to_superuser(client, load_initial_data):
    # Initial count of users
    users_initial_count = User.objects.count()

    # Step 1: Create a normal user via the signup process
    response = client.post(reverse('account_signup'), USER_DATA)
    
    # Validate that the signup was successful
    assert response.status_code == 302  # Assuming signup redirects on success
    assert User.objects.count() == users_initial_count + 1
    
    # Fetch the newly created user
    new_user = User.objects.get(email=USER_DATA['email'])
    
    # Verify the user is not yet a superuser
    assert not new_user.is_superuser
    assert not new_user.is_staff

    # Step 2: Upgrade the user to a superuser
    new_user.is_superuser = True
    new_user.is_staff = True
    new_user.save()

    # Verify the user is now a superuser and staff
    updated_user = User.objects.get(email=USER_DATA['email'])
    assert updated_user.is_superuser
    assert updated_user.is_staff