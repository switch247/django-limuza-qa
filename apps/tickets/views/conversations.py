from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import ConversationEmail, ConversationCall, ConversationChat, Ticket
from ..forms import ConversationEmailForm, ConversationCallForm, ConversationChatForm

@login_required
def download_call_recording(request, conversation_id):
    # this should get the file from s3 
    conversation = get_object_or_404(ConversationCall, id=conversation_id)
    if not conversation.call_recording:
        return HttpResponse("No call recording found.", status=404)
    
    response = FileResponse(conversation.call_recording.open('rb'), content_type='audio/mpeg')
    response['Content-Disposition'] = f'attachment; filename="{conversation.call_recording.name}"'
    return response

@login_required
def view_call_transcription(request, conversation_id):
    conversation = get_object_or_404(ConversationCall, id=conversation_id)
    if not conversation.call_transcription:
        return HttpResponse("No call transcription found.", status=404)
    
    return render(request, 'conversations/view_call_transcription.html', {'conversation': conversation})

@login_required
def create_email_conversation(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ConversationEmailForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.ticket = ticket
            conversation.save()
            return redirect('ticket_details', ticket_id=ticket_id)
    else:
        form = ConversationEmailForm()
    return render(request, 'conversations/create_email_conversation.html', {'form': form, 'ticket': ticket})

@login_required
def create_call_conversation(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ConversationCallForm(request.POST, request.FILES)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.ticket = ticket
            conversation.save()
            return redirect('ticket_details', ticket_id=ticket_id)
    else:
        form = ConversationCallForm()
    return render(request, 'conversations/create_call_conversation.html', {'form': form, 'ticket': ticket})

@login_required
def create_chat_conversation(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ConversationChatForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.ticket = ticket
            conversation.save()
            return redirect('ticket_details', ticket_id=ticket_id)
    else:
        form = ConversationChatForm()
    return render(request, 'conversations/create_chat_conversation.html', {'form': form, 'ticket': ticket})

@login_required
def update_email_conversation(request, conversation_id):
    conversation = get_object_or_404(ConversationEmail, id=conversation_id)
    if request.method == 'POST':
        form = ConversationEmailForm(request.POST, instance=conversation)
        if form.is_valid():
            form.save()
            return redirect('ticket_details', ticket_id=conversation.ticket.id)
    else:
        form = ConversationEmailForm(instance=conversation)
    return render(request, 'conversations/update_email_conversation.html', {'form': form, 'conversation': conversation})

@login_required
def update_call_conversation(request, conversation_id):
    conversation = get_object_or_404(ConversationCall, id=conversation_id)
    if request.method == 'POST':
        form = ConversationCallForm(request.POST, request.FILES, instance=conversation)
        if form.is_valid():
            form.save()
            return redirect('ticket_details', ticket_id=conversation.ticket.id)
    else:
        form = ConversationCallForm(instance=conversation)
    return render(request, 'conversations/update_call_conversation.html', {'form': form, 'conversation': conversation})

@login_required
def update_chat_conversation(request, conversation_id):
    conversation = get_object_or_404(ConversationChat, id=conversation_id)
    if request.method == 'POST':
        form = ConversationChatForm(request.POST, instance=conversation)
        if form.is_valid():
            form.save()
            return redirect('ticket_details', ticket_id=conversation.ticket.id)
    else:
        form = ConversationChatForm(instance=conversation)
    return render(request, 'conversations/update_chat_conversation.html', {'form': form, 'conversation': conversation})

@login_required
def delete_conversation(request, conversation_id, conversation_type):
    if conversation_type == 'email':
        model = ConversationEmail
    elif conversation_type == 'call':
        model = ConversationCall
    elif conversation_type == 'chat':
        model = ConversationChat
    else:
        return HttpResponse("Invalid conversation type.", status=400)

    conversation = get_object_or_404(model, id=conversation_id)
    if request.method == 'POST':
        ticket_id = conversation.ticket.id
        conversation.delete()
        return redirect('ticket_details', ticket_id=ticket_id)
    return render(request, 'conversations/delete_conversation.html', {'conversation': conversation})
