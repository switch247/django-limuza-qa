import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.tickets.models.integrations import Integration
from apps.tickets.models import Ticket, Conversation, ConversationCall, ConversationChat, ConversationEmail
from django.db import IntegrityError
from apps.customer_accounts.test_utils import *
from apps.test_utils import *
from unittest.mock import patch
from datetime import datetime, timedelta
from django.urls import reverse
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant
import json

def load_mock_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

    

User = get_user_model()
def setup_tickets():
    user, workspace, integration = get_dummy_integration()

    set_current_tenant(workspace.account)
    agents = MockCRM.get_mock_agents(integration)
    for agent_data in agents:
        User.objects.create(
            username=agent_data['contact']['name'],
            email=agent_data['contact']['email'],
            external_id=agent_data['id'],
            password='password'  # or use a more secure way to set passwords
        )
    new_tickets = MockCRM.get_mock_tickets(integration)
    for ticket_data in new_tickets:
        user = User.objects.get(external_id=ticket_data['responder_id'])
        ticket = Ticket.objects.create(
            external_id=ticket_data['id'],
            external_agent_id=ticket_data['responder_id'],
            subject=ticket_data['subject'],
            agent = user,
            created_at=datetime.strptime(ticket_data['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
            status=ticket_data['status'],
            ticket_data=ticket_data,
            html_ticket="<p>Test HTML</p>",
            text_ticket="Test Text",
            integration=integration
        )
        for conversation in ticket_data['conversations']:
            Conversation.objects.create(
                ticket=ticket,
                agent = user,
                incoming=conversation['incoming'],
                private=conversation['private'],
                source=conversation['source'],
                external_agent_id=conversation['user_id'],
                body=conversation['body'],
                body_text=conversation['body_text'],
                from_email=conversation['from_email'],
                additional_data=conversation,
                external_id = conversation['id']
            )

    unset_current_tenant()
    return user, workspace, integration

@pytest.mark.django_db
def test_ticket_creation_with_existing_user(basic_test_user_and_account,workspace_for_test_user, test_freshdesk_integration ):
    # Create a user with an external_id
    user,account  = basic_test_user_and_account
    set_current_tenant(account)
    workspace = workspace_for_test_user
    integration = test_freshdesk_integration
    user.external_id = 'agent_1003'
    user.save()
    # Create an integration instance
    
    # Create a ticket with the same external_id as the user
    ticket = Ticket.objects.create(
        external_id='external_1003',
        external_agent_id='agent_1003',
        subject="Migrate my account to my own workspace",
        integration=integration,
        agent = user,
        status="open",
        ticket_data={"priority": 4, "requester_id": 151023139807},
        html_ticket="<p>Test HTML</p>",
        text_ticket="Test Text",
        created_at=timezone.now()
    )
    # Fetch the ticket from the database to ensure it's saved correctly
    ticket.refresh_from_db()

    # Check that the agent field is set to the correct user
    unset_current_tenant()
    assert ticket.agent == user

@pytest.mark.django_db
def test_ticket_creation_without_account(basic_test_user_and_account,workspace_for_test_user, test_freshdesk_integration):
    # Create a workspace instance
    user,_ = basic_test_user_and_account
    workspace = workspace_for_test_user
    integration = test_freshdesk_integration
    # Create an integration instance associated with the workspace
    try:
        Ticket.objects.create(
            external_id='nonexistent_external_id',
            external_agent_id='nonexistent_agent_id',
            subject="Migrate my account to my own workspace",
            integration=integration,
            agent = user,
            status="open",
            ticket_data={"priority": 4, "requester_id": 151023139807},
            html_ticket="<p>Test HTML</p>",
            text_ticket="Test Text",
            created_at=timezone.now()
        )
    except IntegrityError as e:
        account_substring = 'null value in column "account_id" of relation'
        assert account_substring in str(e)

# TODO write test that checks if tickets include conversations


@pytest.mark.django_db
def test_create_tickets_with_mock_agents_and_tickets(basic_test_user_and_account,workspace_for_test_user, test_freshdesk_integration):

    #TODO fix ticket.agents so that its optional. There should be a ticket.agent_email which is mandatory but ticket.agent which isn't.

    """
    Given a valid and active CRM integration,
    And there are new agents and tickets available in CRM,
    When the background job runs to fetch new agents and tickets,
    Then the new agents are fetched and users are created,
    And the new tickets are retrieved from CRM,
    And the tickets are processed and stored in the system,
    And each ticket's original data is stored in the ticket_data field,
    And each ticket is associated with the correct integration.
    """
    # Given
    user,account = basic_test_user_and_account
    workspace = workspace_for_test_user
    integration = test_freshdesk_integration
    set_current_tenant(account)


    # Fetch tickets
    new_tickets = load_mock_data('apps/tickets/fixtures/mock_tickets.json')
    conversations = load_mock_data('apps/tickets/fixtures/mock_conversation.json')

    # Attach conversations to the tickets
    for ticket in new_tickets:
        ticket['conversations'] = [
            conversation for conversation in conversations
            if conversation['ticket_id'] == ticket['id']
        ]

    for ticket_data in new_tickets:
        user = User.objects.get(external_id=ticket_data['responder_id'])
        ticket = Ticket.objects.create(
            external_id=ticket_data['id'],
            external_agent_id=ticket_data['responder_id'],
            subject=ticket_data['subject'],
            agent = user,
            created_at=datetime.strptime(ticket_data['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
            status=ticket_data['status'],
            ticket_data=ticket_data,
            html_ticket="<p>Test HTML</p>",
            text_ticket="Test Text",
            integration=integration
        )
        for conversation in ticket_data['conversations']:
            Conversation.objects.create(
                ticket=ticket,
                agent = user,
                incoming=conversation['incoming'],
                private=conversation['private'],
                source=conversation['source'],
                external_agent_id=conversation['user_id'],
                body=conversation['body'],
                body_text=conversation['body_text'],
                from_email=conversation['from_email'],
                additional_data=conversation,
                external_id = conversation['id']
            )
        assert Conversation.objects.filter(ticket=ticket).count() == len(ticket_data['conversations'])
        assert Ticket.objects.filter(id=ticket.id).exists()
        assert ticket.ticket_data is not None
        assert ticket.integration == integration
        assert ticket.agent is not None  # Ensure the agent field is populated


@pytest.mark.django_db
def test_ticket_deletion(basic_test_user_and_account,workspace_for_test_user, test_freshdesk_integration):
    """
    Test deleting a ticket and ensure related conversations are also deleted.
    """
    user,account = basic_test_user_and_account
    workspace = workspace_for_test_user
    integration = test_freshdesk_integration
    set_current_tenant(account)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_3000',
        external_agent_id='agent_3000',
        subject="Delete this ticket",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 2, "requester_id": 171023139807},
        html_ticket="<p>Delete this ticket</p>",
        text_ticket="Delete this ticket",
        created_at=timezone.now()
    )

    # Create a conversation related to the ticket
    ConversationEmail.objects.create(
        ticket=ticket,
        agent=user,
        incoming=True,
        private=False,
        source=1,
        body="Email conversation body",
        body_text="Email conversation text",
        from_email="test@example.com",
        additional_data={"extra": "data"},
        external_id="conversation_3000",
        title="Email Conversation Title"
    )

    # Ensure the ticket and conversation are created
    assert Ticket.objects.filter(id=ticket.id).exists()
    assert Conversation.objects.filter(ticket=ticket).exists()

    # Delete the ticket
    ticket.delete()

    # Ensure the ticket and conversation are deleted
    assert not Ticket.objects.filter(id=ticket.id).exists()
    assert not Conversation.objects.filter(ticket=ticket).exists()

@pytest.mark.django_db
def test_ticket_update(basic_test_user_and_account,workspace_for_test_user, test_freshdesk_integration):
    """
    Test updating a ticket's subject and status.
    """
    user,account = basic_test_user_and_account
    workspace = workspace_for_test_user
    integration = test_freshdesk_integration
    set_current_tenant(account)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_4000',
        external_agent_id='agent_4000',
        subject="Original Subject",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 1, "requester_id": 181023139807},
        html_ticket="<p>Original HTML</p>",
        text_ticket="Original Text",
        created_at=timezone.now()
    )

    # Update the ticket's subject and status
    ticket.subject = "Updated Subject"
    ticket.status = "closed"
    ticket.save()

    # Refresh from the database to verify changes
    ticket.refresh_from_db()

    # Ensure the ticket is updated
    assert ticket.subject == "Updated Subject"
    assert ticket.status == "closed"

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
def test_conversation_creation_for_ticket(basic_test_user_and_account,workspace_for_test_user, test_freshdesk_integration):
    """
    Test creating a conversation associated with a ticket.
    """
    user,account = basic_test_user_and_account
    workspace = workspace_for_test_user
    integration = test_freshdesk_integration
    set_current_tenant(account)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_5000',
        external_agent_id='agent_5000',
        subject="Ticket with conversation",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 2, "requester_id": 191023139807},
        html_ticket="<p>HTML content</p>",
        text_ticket="Text content",
        created_at=timezone.now()
    )

    # Create a conversation related to the ticket
    conversation = ConversationChat.objects.create(
        ticket=ticket,
        agent=user,
        incoming=True,
        private=False,
        source=1,
        body="Chat conversation body",
        body_text="Chat conversation text",
        external_agent_id='agent_5000',
        chat_platform="WhatsApp",
        external_id="conversation_5000"
    )

    # Ensure the conversation is created and linked to the ticket
    assert Conversation.objects.filter(ticket=ticket, id=conversation.id).exists()
    assert conversation.chat_platform == "WhatsApp"

@pytest.mark.django_db
def test_download_call_recording(client, basic_test_user_and_account,workspace_for_test_user, test_freshdesk_integration):
    """
    Test downloading a call recording associated with a conversation.
    """
    user,account = basic_test_user_and_account
    workspace = workspace_for_test_user
    integration = test_freshdesk_integration
    set_current_tenant(account)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_6000',
        external_agent_id='agent_6000',
        subject="Ticket with call recording",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 3, "requester_id": 201023139807},
        html_ticket="<p>HTML content</p>",
        text_ticket="Text content",
        created_at=timezone.now()
    )

    # Create a call conversation with a recording
    conversation = ConversationCall.objects.create(
        ticket=ticket,
        agent=user,
        incoming=False,
        private=False,
        source=1,
        body="Call conversation body",
        body_text="Call conversation text",
        external_agent_id='agent_6000',
        call_recording='path/to/recording.mp3',
        call_transcription="Transcription text",
        external_id="conversation_6000"
    )

    # Simulate a client request to download the call recording
    client.force_login(user)
    response = client.get(f'/conversations/download_call_recording/{conversation.id}/')

    # Check that the response is a file download
    assert response.status_code == 200
    assert response['Content-Disposition'] == f'attachment; filename="{conversation.call_recording.name}"'
