from django.urls import path
from .views import tickets as ticket_views
from .views import conversations as conversation_views
from .views import filters as integration_views

urlpatterns = [
    path('', ticket_views.view_tickets, name='view_tickets'),
    path('fetch-tickets/', ticket_views.fetch_tickets, name='fetch_tickets'),
    path('<int:ticket_id>/', ticket_views.ticket_details, name='ticket_details'),
    path('create/', ticket_views.create_ticket, name='create_ticket'),
    path('<int:ticket_id>/update/', ticket_views.update_ticket, name='update_ticket'),
    path('<int:ticket_id>/delete/', ticket_views.delete_ticket, name='delete_ticket'),
    path('<int:ticket_id>/conversations/email/create/', conversation_views.create_email_conversation, name='create_email_conversation'),
    path('<int:ticket_id>/conversations/call/create/', conversation_views.create_call_conversation, name='create_call_conversation'),
    path('<int:ticket_id>/conversations/chat/create/', conversation_views.create_chat_conversation, name='create_chat_conversation'),
    path('conversations/email/<int:conversation_id>/update/', conversation_views.update_email_conversation, name='update_email_conversation'),
    path('conversations/call/<int:conversation_id>/update/', conversation_views.update_call_conversation, name='update_call_conversation'),
    path('conversations/chat/<int:conversation_id>/update/', conversation_views.update_chat_conversation, name='update_chat_conversation'),
    path('conversations/<str:conversation_type>/<int:conversation_id>/delete/', conversation_views.delete_conversation, name='delete_conversation'),
    path('conversations/call/<int:conversation_id>/download/', conversation_views.download_call_recording, name='download_call_recording'),
    path('conversations/call/<int:conversation_id>/transcription/', conversation_views.view_call_transcription, name='view_call_transcription'),
    path('<str:integration_id>/filter/', integration_views.filter, name='filter'),
    path('<str:integration_id>/do_filter/', integration_views.do_filter, name='do_filter'),
    path('<str:integration_id>create_filter/', integration_views.create_filter, name='create_filter'),
    path('update_filter/<int:filter_id>/', integration_views.update_filter, name='update_filter'),
    path('delete_filter/<int:filter_id>/', integration_views.delete_filter, name='delete_filter'),
    path('view_filter/<int:filter_id>/', integration_views.view_filter, name='view_filter')
]