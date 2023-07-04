import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from apps.tickets.models import Ticket, ConversationCall, ConversationEmail, ConversationChat
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant


@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_download_call_recording_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for downloading a call recording associated with a conversation.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

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
        call_recording=SimpleUploadedFile('recording.mp3', b'test audio content'),
        call_transcription="Transcription text",
        external_id="conversation_6000"
    )

    # Simulate a client request to download the call recording
    client.force_login(user)
    response = client.get(reverse('download_call_recording', args=[conversation.id]))

    # Check that the response is a file download
    assert response.status_code == 200
    assert response['Content-Disposition'] == f'attachment; filename="{conversation.call_recording.name}"'

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_view_call_transcription_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for viewing the call transcription of a conversation.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_6001',
        external_agent_id='agent_6001',
        subject="Ticket with call transcription",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 3, "requester_id": 201023139808},
        html_ticket="<p>HTML content</p>",
        text_ticket="Text content",
        created_at=timezone.now()
    )

    # Create a call conversation with a transcription
    conversation = ConversationCall.objects.create(
        ticket=ticket,
        agent=user,
        incoming=False,
        private=False,
        source=1,
        body="Call conversation body",
        body_text="Call conversation text",
        external_agent_id='agent_6001',
        call_transcription="Test transcription text",
        external_id="conversation_6001"
    )

    # Simulate a client request to view the call transcription
    client.force_login(user)
    response = client.get(reverse('view_call_transcription', args=[conversation.id]))

    # Check that the transcription is displayed in the response
    assert response.status_code == 200
    assert "Test transcription text" in response.content.decode()

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_create_email_conversation_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for creating an email conversation associated with a ticket.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_7000',
        external_agent_id='agent_7000',
        subject="Ticket for email conversation",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 2, "requester_id": 211023139807},
        html_ticket="<p>HTML content</p>",
        text_ticket="Text content",
        created_at=timezone.now()
    )

    # Simulate a client request to create an email conversation
    client.force_login(user)
    response = client.post(
        reverse('create_email_conversation', args=[ticket.id]),
        data={
            'subject': 'Email conversation subject',
            'body': 'Email conversation body',
            'body_text': 'Email conversation text',
            'from_email': 'test@example.com'
        }
    )

    # Ensure the email conversation is created and linked to the ticket
    assert response.status_code == 302
    assert ConversationEmail.objects.filter(ticket=ticket).exists()

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_update_call_conversation_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for updating a call conversation.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_8000',
        external_agent_id='agent_8000',
        subject="Ticket for call conversation update",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 3, "requester_id": 221023139807},
        html_ticket="<p>HTML content</p>",
        text_ticket="Text content",
        created_at=timezone.now()
    )

    # Create a call conversation
    conversation = ConversationCall.objects.create(
        ticket=ticket,
        agent=user,
        incoming=False,
        private=False,
        source=1,
        body="Call conversation body",
        body_text="Call conversation text",
        external_agent_id='agent_8000',
        external_id="conversation_8000"
    )

    # Simulate a client request to update the call conversation
    client.force_login(user)
    response = client.post(
        reverse('update_call_conversation', args=[conversation.id]),
        data={
            'body': 'Updated call conversation body',
            'body_text': 'Updated call conversation text'
        }
    )

    # Ensure the conversation is updated
    conversation.refresh_from_db()
    assert response.status_code == 302
    assert conversation.body == 'Updated call conversation body'
    assert conversation.body_text == 'Updated call conversation text'

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_integrations_and_acc')
@pytest.mark.xfail(reason="not implemented yet")
def test_delete_conversation_integration(client, user_fixture, workspace_fixture, integration_fixture, account_fixture):
    """
    Integration test for deleting a conversation.
    """
    user = user_fixture
    workspace = workspace_fixture
    integration = integration_fixture
    set_current_tenant(account_fixture)

    # Create a ticket
    ticket = Ticket.objects.create(
        external_id='external_9000',
        external_agent_id='agent_9000',
        subject="Ticket for conversation deletion",
        integration=integration,
        agent=user,
        status="open",
        ticket_data={"priority": 4, "requester_id": 231023139807},
        html_ticket="<p>HTML content</p>",
        text_ticket="Text content",
        created_at=timezone.now()
    )

    # Create a chat conversation
    conversation = ConversationChat.objects.create(
        ticket=ticket,
        agent=user,
        incoming=True,
        private=False,
        source=1,
        body="Chat conversation body",
        body_text="Chat conversation text",
        external_agent_id='agent_9000',
        chat_platform="WhatsApp",
        external_id="conversation_9000"
    )

    # Simulate a client request to delete the conversation
    client.force_login(user)
    response = client.post(reverse('delete_conversation', args=[conversation.id, 'chat']))

    # Ensure the conversation is deleted
    assert response.status_code == 302
    assert not ConversationChat.objects.filter(id=conversation.id).exists()


@pytest.mark.integration
@pytest.mark.xfail(reason="not implemented yet")
def test_transcribe_call_integration():
    # test service method
    #should only run on production environment
    assert 'transcription_text' == 'conversation.transcription_text'