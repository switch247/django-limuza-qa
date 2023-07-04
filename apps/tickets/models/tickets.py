from django.db import models
from django.conf import settings
from apps.tickets.models.integrations import Integration
from django.contrib.auth import get_user_model
from apps.customer_accounts.models import TenantClass, TenantForeignKey

User = get_user_model()

class Ticket(TenantClass):
    """
    Model representing a support ticket.

    Attributes:
        external_id (str): External identifier for the ticket, typically from an integrated CRM or helpdesk system.
        subject (str): The subject or title of the ticket.
        integration (Integration): Foreign key to the Integration model, representing the integration source of the ticket.
        external_agent_id (str): External identifier for the agent associated with the ticket, used when the agent is managed externally.
        agent (User): The internal agent assigned to the ticket.
        created_at (datetime): The date and time when the ticket was created.
        status (str): The current status of the ticket (e.g., open, closed, pending).
        is_call (bool): Boolean field indicating whether the ticket is related to a call.
        ticket_data (JSON): A JSON field to store additional ticket data, such as metadata from the integration source.
        html_ticket (str): The HTML content of the ticket, typically representing the formatted message.
        text_ticket (str): The plain text content of the ticket.

    Methods:
        save(*args, **kwargs): Custom save method to assign the internal agent based on the external agent ID.
        __str__(): Returns the string representation of the ticket, which is the subject.
        mark_as_call(): Marks the ticket as related to a call and saves the change.
    """

    external_id = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    integration = TenantForeignKey(Integration, on_delete=models.PROTECT)
    external_agent_id = models.CharField(max_length=255)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='tickets'
    )
    created_at = models.DateTimeField()
    status = models.CharField(max_length=50)
    is_call = models.BooleanField(default=False)  # Field to mark call tickets
    ticket_data = models.JSONField()
    html_ticket = models.TextField()
    text_ticket = models.TextField()

    def save(self, *args, **kwargs):
        if self.external_agent_id and not self.agent:
            try:
                self.agent = User.objects.get(external_id=self.external_agent_id)
            except User.DoesNotExist:
                raise ValueError(f"User with external_id {self.external_agent_id} does not exist")
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject

    def mark_as_call(self):
        self.is_call = True
        self.save()


class Conversation(TenantClass):
    """
    Model representing a conversation within a ticket.

    Attributes:
        external_id (str): External identifier for the conversation, typically from an integrated CRM or helpdesk system.
        external_agent_id (str): External identifier for the agent associated with the conversation, if managed externally.
        ticket (Ticket): Foreign key to the Ticket model, linking the conversation to a specific ticket.
        incoming (bool): Boolean field indicating whether the conversation is incoming (from the customer) or outgoing (from the agent).
        private (bool): Boolean field indicating whether the conversation is private (not visible to the customer).
        source (int): An integer representing the source of the conversation (e.g., email, chat, call).
        agent (User): The internal agent associated with the conversation.
        body (str): The content of the conversation, typically in HTML or rich text format.
        body_text (str): The plain text version of the conversation content.
        from_email (str, optional): Email address from which the conversation originated, if applicable.
        additional_data (JSON, optional): A JSON field to store any additional data related to the conversation.

    Subclasses:
        ConversationEmail: Model for email conversations, with a title attribute.
        ConversationCall: Model for call conversations, with fields for call recording and transcription.
        ConversationChat: Model for chat conversations, with a field for the chat platform.
    """

    external_id = models.CharField(max_length=255)
    external_agent_id = models.CharField(max_length=255, null=True)
    ticket = TenantForeignKey(Ticket, related_name='conversations', on_delete=models.PROTECT)
    incoming = models.BooleanField()
    private = models.BooleanField()
    source = models.IntegerField()
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='conversations'
    )
    body = models.TextField()
    body_text = models.TextField()
    from_email = models.EmailField(null=True)
    additional_data = models.JSONField(null=True, blank=True)


class ConversationEmail(Conversation):
    """
    Model representing an email conversation.

    Inherits from Conversation and adds:
        title (str): The subject or title of the email conversation.
    """

    title = models.TextField()


class ConversationCall(Conversation):
    """
    Model representing a call conversation.

    Inherits from Conversation and adds:
        call_recording (FileField, optional): File field to store the call recording.
        call_transcription (str, optional): Text field to store the transcription of the call.
    """

    call_recording = models.FileField(upload_to='call_recordings/', null=True, blank=True)
    call_transcription = models.TextField(null=True, blank=True)
    call_transcription_data = models.JSONField(null=True, blank=True)
#TODO carry on work here ISSUE17

class ConversationChat(Conversation):
    """
    Model representing a chat conversation.

    Inherits from Conversation and adds:
        chat_platform (str): The platform on which the chat took place (e.g., WhatsApp, Facebook Messenger).
    """

    chat_platform = models.CharField(max_length=50)
