import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.tickets.models.integrations import Integration
from apps.tickets.models import Ticket, Conversation
from django.db import IntegrityError
from apps.customer_accounts.test_utils import *
from apps.test_utils import *
from unittest.mock import patch
from datetime import datetime, timedelta
from django.urls import reverse
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant
import json

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_view_tickets_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for viewing a list of tickets.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create tickets
    ticket1 = Ticket.objects.create(
        external_id='external_10000',
        external_agent_id='agent_10000',
        subject="Ticket 1",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 4, "requester_id": 241023139807},
        html_ticket="<p>HTML content 1</p>",
        text_ticket="Text content 1",
        created_at=timezone.now()
    )

    ticket2 = Ticket.objects.create(
        external_id='external_10001',
        external_agent_id='agent_10001',
        subject="Ticket 2",
        integration=integration,
        agent=user,
        status="closed",
        ticket_data={"priority": 3, "requester_id": 251023139807},
        html_ticket="<p>HTML content 2</p>",
        text_ticket="Text content 2",
        created_at=timezone.now()
    )

    # Simulate a client request to view tickets
    client.force_login(user)
    response = client.get(reverse('view_tickets'))

    # Check that the response contains the ticket details
    assert response.status_code == 200
    assert "Ticket 1" in response.content.decode()
    assert "Ticket 2" in response.content.decode()

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_ticket_details_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for viewing the details of a specific ticket.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_11000',
        external_agent_id='agent_11000',
        subject="Ticket Details",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 2, "requester_id": 261023139807},
        html_ticket="<p>Ticket details HTML content</p>",
        text_ticket="Ticket details text content",
        created_at=timezone.now()
    )

    # Simulate a client request to view the ticket details
    client.force_login(user)
    response = client.get(reverse('ticket_details', args=[ticket.id]))

    # Check that the response contains the correct ticket details
    assert response.status_code == 200
    assert "Ticket Details" in response.content.decode()
    assert "Ticket details text content" in response.content.decode()

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_create_ticket_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for creating a new ticket.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Simulate a client request to create a new ticket
    client.force_login(user)
    response = client.post(
        reverse('create_ticket'),
        data={
            'external_id': 'external_12000',
            'external_agent_id': 'agent_12000',
            'subject': 'New Ticket',
            'status': 'open',
            'ticket_data': '{"priority": 1, "requester_id": 271023139807}',
            'html_ticket': '<p>New ticket HTML content</p>',
            'text_ticket': 'New ticket text content',
            'created_at': timezone.now(),
            'integration': integration.id,
            'agent': user.id,
            'is_call': 'on'
        }
    )

    # Ensure the ticket is created and redirected to the ticket list
    assert response.status_code == 302
    assert Ticket.objects.filter(subject='New Ticket').exists()

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_update_ticket_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for updating an existing ticket.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_13000',
        external_agent_id='agent_13000',
        subject="Ticket to Update",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 2, "requester_id": 281023139807},
        html_ticket="<p>Update ticket HTML content</p>",
        text_ticket="Update ticket text content",
        created_at=timezone.now()
    )

    # Simulate a client request to update the ticket
    client.force_login(user)
    response = client.post(
        reverse('update_ticket', args=[ticket.id]),
        data={
            'subject': 'Updated Ticket',
            'status': 'closed',
            'ticket_data': '{"priority": 3, "requester_id": 291023139807}',
            'html_ticket': '<p>Updated ticket HTML content</p>',
            'text_ticket': 'Updated ticket text content',
            'is_call': 'on'
        }
    )

    # Ensure the ticket is updated and redirected to the ticket details
    ticket.refresh_from_db()
    assert response.status_code == 302
    assert ticket.subject == 'Updated Ticket'
    assert ticket.status == 'closed'

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
def test_delete_ticket_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for deleting a ticket.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_14000',
        external_agent_id='agent_14000',
        subject="Ticket to Delete",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 4, "requester_id": 301023139807},
        html_ticket="<p>Delete ticket HTML content</p>",
        text_ticket="Delete ticket text content",
        created_at=timezone.now()
    )

    # Simulate a client request to delete the ticket
    client.force_login(user)
    response = client.post(reverse('delete_ticket', args=[ticket.id]))

    # Ensure the ticket is deleted and redirected to the ticket list
    assert response.status_code == 302
    assert not Ticket.objects.filter(id=ticket.id).exists()