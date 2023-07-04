# test_utils.py

import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from apps.customer_accounts.models import Workspace
from django.contrib.auth import get_user_model
from apps.tickets.models.integrations import Integration, FreshdeskIntegration
from apps.tickets.services import *
from apps.customer_accounts.test_utils import *
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant


User = get_user_model()

class MockResponse:
    """
    Mock response class.

    This class is used to mock API responses from external services.
    """
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

class MockCRM:
    @staticmethod
    def load_mock_data(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    @staticmethod
    def mock_api_call_to_fetch_tickets(api_key, last_updated_at):
        tickets = MockCRM.load_mock_data('apps/integrations/tests/mock_data/tickets.json')
        conversations = MockCRM.load_mock_data('apps/integrations/tests/mock_data/conversations.json')

        # Filter tickets based on last_updated_at
        filtered_tickets = [
            ticket for ticket in tickets
            if datetime.strptime(ticket['updated_at'], '%Y-%m-%dT%H:%M:%SZ') > last_updated_at
        ]

        # Attach conversations to the tickets
        for ticket in filtered_tickets:
            ticket['conversations'] = [
                conversation for conversation in conversations
                if conversation['ticket_id'] == ticket['id']
            ]

        return MockResponse({"tickets": filtered_tickets})

    @staticmethod
    def mock_api_call_to_fetch_agents(api_key):
        agents = MockCRM.load_mock_data('apps/integrations/tests/mock_data/agents.json')
        return MockResponse({"agents": agents})

    @staticmethod
    def get_mock_agents(integration):
        response = MockCRM.mock_api_call_to_fetch_agents(integration.integration_key)
        if response.status_code == 200:
            agents = response.json().get('agents', [])
            return agents
        return []

    @staticmethod
    def get_mock_tickets(integration, last_updated_at=None):
        if last_updated_at is None:
            last_updated_at = datetime.now() - timedelta(days=1000)
        response = MockCRM.mock_api_call_to_fetch_tickets(integration.integration_key, last_updated_at)
        if response.status_code == 200:
            tickets = response.json().get('tickets', [])
            return tickets
        return []

# Helper functions


def create_test_integration(workspace, integration_name="Test Integration", active=True):
    set_current_tenant(workspace.account)
    fd_int =  FreshdeskIntegration.objects.create(
        workspace=workspace,
        name=integration_name,
        active=active,
        details={
            "api_key": "fake_api_key",
            "url": "https://api.fake-crm.com"
        }
    )
    unset_current_tenant()
    return fd_int

def get_fake_integration_json(name="Test CRM Integration", type="freshdesk", integration_key="fake_key", active=True):
    return {
        "name": name,
        "type": type,
        "integration_key": integration_key,
        "active": active,
        "details": {
            "api_key": "fake_api_key",
            "url": "https://api.fake-crm.com"
        }
    }

def get_dummy_integration():
    dummy_integration_data = get_fake_integration_json()
    user, account, workspace = create_admin_user_and_account(admin=True)
    set_current_tenant(account)
    integration = setup_crm_integration(user, workspace, dummy_integration_data)
    unset_current_tenant()
    return user, workspace, integration
