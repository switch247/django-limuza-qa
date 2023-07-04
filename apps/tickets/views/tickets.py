from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Ticket
from django.contrib.auth import get_user_model
from ..forms import TicketForm 
from datetime import datetime, timedelta # ADDED BY SMARTDEV-CODE
from django.utils import timezone # ADDED BY SMARTDEV-CODE
User = get_user_model()

# ADDED BY SMARTDEV-CODE
import json
from django.conf import settings 
from pathlib import Path
from datetime import datetime
# ADDED BY SMARTDEV-CODE END

@login_required
def view_tickets(request):
    #if filter, then user the filter request
    #else get tickets:
    # Fetch the latest 10 tickets from the database
    tickets = Ticket.objects.select_related('account').order_by('-created_at')[:10]
    # LOAD TEMPORARY CHAT FROM JSON
    chats_data = []
    json_file_path_chat = Path(settings.BASE_DIR) / 'limuza' / 'data' / 'chats.json'
    try:
        with open(json_file_path_chat) as f:
            chats_data = json.load(f)
        
    except FileNotFoundError:
        chats_data = []
        # print(f"File not found: {json_file_path}")
  
    
    initial_ticket = tickets[0] if tickets else None
    return render(request, 'index.html', {'tickets': tickets, 'ticket': initial_ticket, 'chats': chats_data})

@login_required
def fetch_tickets(request):
    filter_by = request.GET.get('filter_by', None)
    tickets = Ticket.objects.select_related('account').all()  # Default queryset

    try:
        if filter_by == 'last_7_days':
            tickets = tickets.filter(created_at__gte=timezone.now() - timedelta(days=7))
        elif filter_by == 'all_status':
            # Assuming you want to show all tickets regardless of status
            pass  # `tickets` already contains all tickets
        elif filter_by == 'all_users':
            # Show tickets for all users
            pass  # `tickets` already contains all tickets
        elif filter_by == 'newest':
            tickets = tickets.order_by('-created_at')
        else:
            # Handle any other unknown filter values
            pass
    except Exception as e:
        # Log the exception (in a real app, use logging instead of print)
        print(f"Error filtering tickets: {e}")
        # Optionally, you could return an error message or a different template here

    # Render the filtered tickets in a template fragment
    return render(request, '_ticket_list.html', {'tickets': tickets})

@login_required
def ticket_details(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # LOAD TEMPORARY CHATS
    chats_data = []
    json_file_path_chat = Path(settings.BASE_DIR) / 'limuza' / 'data' / 'chats.json'
    try:
        with open(json_file_path_chat) as f:
            chats_data = json.load(f)
        
    except FileNotFoundError:
        chats_data = []
    return render(request, '_ticket.html', {'ticket': ticket, 'chats': chats_data})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.account_id = request.user.id
            ticket.save()
            if 'is_call' in request.POST and request.POST['is_call'] == 'on':
                ticket.mark_as_call()
            return redirect('view_tickets')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            if 'is_call' in request.POST and request.POST['is_call'] == 'on':
                ticket.mark_as_call()
            return redirect('ticket_details', ticket_id=ticket_id)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/update_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('view_tickets')
    
    return render(request, 'tickets/delete_ticket.html', {'ticket': ticket})
