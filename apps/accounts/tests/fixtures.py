import pytest
from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress

from apps.customer_accounts import models
from apps.customer_accounts import apps

User = get_user_model()


@pytest.fixture
def load_initial_data():
    '''this loads the same as management command initial_setup'''
    roles_list = apps.ROLES
    for role in roles_list:
        models.Role.objects.create(**role)

    subscription_plans_list = apps.SUBSCRIPTION_PLANS
    for plan in subscription_plans_list:
        models.SubscriptionPlan.objects.create(**plan)
    return models.Role.objects.count(), models.SubscriptionPlan.objects.count()


@pytest.fixture
def basic_customer_account():
    """
    Fixture to create an Account for tests.
    """
    account, _ = models.CustomerAccount.objects.get_or_create(name='testaccount')
    return account


@pytest.fixture
def basic_workspace(load_initial_data, basic_customer_account):
    """
    Fixture to create a Workspace for tests.
    """
    workspace = models.Workspace.objects.create(
        name='Test Workspace',
        account=basic_customer_account,
        description='A description of the new workspace'
    )
    return workspace

@pytest.fixture
def basic_test_user_and_account(load_initial_data):
    user = get_user_model().objects.create_user(
        email='james.bond@examle.com',
        password='topsecret',
        username='james.bond',
        first_name='James',
        last_name='Bond'
    )
    account = user.profile.account
    EmailAddress.objects.create(
        user=user,
        email=user.email,
        primary=True,
        verified=True
    )
    return user, account


@pytest.fixture
def workspace_for_test_user(basic_test_user_and_account):
    _, account = basic_test_user_and_account
    workspace = models.Workspace.objects.create(
        name='Test Workspace for  test user',
        account=account,
        description='A special workspace for test user'
    )
    return workspace
