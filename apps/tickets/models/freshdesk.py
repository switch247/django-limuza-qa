from django.db import models
from .tickets import Ticket, Conversation

class FreshdeskTicket(Ticket):
    description = models.TextField()
    description_text = models.TextField()

class FreshdeskEmailConversation(Conversation):
    title = models.TextField()

class FreshdeskCallConversation(Conversation):
    call_recording = models.FileField(upload_to='call_recordings/', null=True, blank=True)
    call_transcription = models.TextField(null=True, blank=True)

class FreshdeskChatConversation(Conversation):
    chat_platform = models.CharField(max_length=50)
