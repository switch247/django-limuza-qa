# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.tickets.models import Ticket, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_save, sender=Ticket)
def set_ticket_agent(sender, instance, **kwargs):
    if instance.external_agent_id and not instance.agent:
        try:
            instance.agent = User.objects.get(external_id=instance.external_agent_id)
        except User.DoesNotExist:
            raise ValueError(f"User with external_id {instance.external_agent_id} does not exist")

@receiver(pre_save, sender=Conversation)
def set_conversation_agent(sender, instance, **kwargs):
    if instance.external_agent_id and not instance.agent:
        try:
            instance.agent = User.objects.get(external_id=instance.external_agent_id)
        except User.DoesNotExist:
            raise ValueError(f"User with external_id {instance.external_agent_id} does not exist")
