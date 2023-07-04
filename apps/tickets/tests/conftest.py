import json
import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from apps.customer_accounts.middleware import MultitenantMiddleware
from django.core.management import call_command
from apps.customer_accounts.models import CustomerAccount, Workspace
from apps.tickets.models.integrations import Integration, FreshdeskIntegration
from django.test import RequestFactory
import yaml
from apps.test_utils import *
from apps.customer_accounts.tests.fixtures import basic_test_user_and_account,workspace_for_test_user
# Import conftest from apps/accounts/tests
User = get_user_model()



@pytest.fixture
def test_freshdesk_integration(basic_test_user_and_account, workspace_for_test_user):
    user,account = basic_test_user_and_account
    return create_test_integration(workspace=workspace_for_test_user)