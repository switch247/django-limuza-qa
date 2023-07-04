from django.shortcuts import render

from ..services import filter_tickets
from ..models.integrations import FreshdeskIntegration, Integration, SavedFilter
from ..models import Ticket
from ..forms import DynamicTicketFilterForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
User = get_user_model()
# def receive_ticket_from_freshdesk(request):
#     # Assuming you have parsed raw_data from the request
#     raw_data = {
#         # Example raw_data payload
#         "id": "330794",
#         "subject": "how to adjust leave balances as well as take on balances",
#         "status": 5,
#         "created_at": "2024-01-24T11:19:31Z",
#         "description": "<pre>The following message...</pre>",
#         "description_text": "The following message...",
#         "ticket_data": raw_data,
#         # Additional fields
#     }
    
#     integration = FreshdeskIntegration.objects.get(id=1)  # Example integration instance
#     agent = User.objects.get(id=1)  # Example agent instance

#     ticket, created = process_ticket_data(
#         external_id=raw_data['id'],
#         subject=raw_data['subject'],
#         agent=agent,
#         status=raw_data['status'],
#         ticket_data=raw_data,
#         html_ticket=raw_data['description'],
#         text_ticket=raw_data['description_text'],
#         integration=integration
#     )

#     if created:
#         # Do something if the ticket was created
#         pass
#     else:
#         # Do something if the ticket was updated
#         pass



def filter(request, integration_id):
    """
    View handles GET and POST requests for filtering tickets.
    
    Args:
        request: The HTTP request object containing filter parameters or a saved filter name.
        integration_id: The ID of the integration to filter tickets for.

    Returns:
        A rendered template with the filtered tickets and the filter form.
    """
    integration = get_object_or_404(Integration, id=integration_id)
    
    if request.method == 'GET':
        form = DynamicTicketFilterForm(None, integration=integration)
        return render(request, 'ticket_filter.html', {'form': form, 'tickets': [], 'integration': integration})

    elif request.method == 'POST':
        if 'filter_id' in request.POST:
            saved_filter = get_object_or_404(SavedFilter, id=request.POST['filter_id'], integration=integration, user=request.user)
            filter_data = saved_filter.filter_data
        else:
            form = DynamicTicketFilterForm(request.POST, integration=integration)
            if form.is_valid():
                filter_data = form.cleaned_data
            else:
                return render(request, 'ticket_filter.html', {'form': form, 'tickets': []})

        return do_filter(request, integration, filter_data)

        
def do_filter(request, integration, filter_data):
    """
    Filters tickets based on provided filter data and returns results.
    Handles pagination and different response formats (HTMX, JSON).

    Args:
        request: The HTTP request object.
        integration: The integration instance to filter tickets for.
        filter_data: A dictionary containing filter criteria.

    Returns:
        A response with the filtered tickets.
    """
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    paginated_tickets = filter_tickets(filter_data, integration, page, page_size)

    if request.headers.get('hx-request') == 'true':
        return render(request, '_ticket_list.html', {'tickets': paginated_tickets, 'integration': integration})
    
    if request.headers.get('content-type') == 'application/json':
        tickets_data = list(paginated_tickets.object_list.values())
        return JsonResponse({
            'tickets': tickets_data,
            'page': paginated_tickets.number,
            'num_pages': paginated_tickets.paginator.num_pages,
        })

    form = DynamicTicketFilterForm(None, integration=integration)
    return render(request, 'ticket_filter.html', {'form': form, 'tickets': paginated_tickets, 'integration': integration})

def create_filter(request, integration_id):
    integration = get_object_or_404(Integration, id=integration_id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = DynamicTicketFilterForm(request.POST, integration=integration)
        if form.is_valid():
            filter_name = request.POST.get('filter_name')
            filter_data = form.cleaned_data
            SavedFilter.objects.create(
                user=user,
                integration=integration,
                filter_data=filter_data,
                name=filter_name
            )
            return redirect('filter', integration_id=integration_id)
    
    form = DynamicTicketFilterForm(None, integration=integration)
    return render(request, 'filters/create.html', {'form': form, 'integration': integration})

def update_filter(request, filter_id):
    saved_filter = get_object_or_404(SavedFilter, id=filter_id, user=request.user)
    integration = saved_filter.integration
    
    if request.method == 'POST':
        form = DynamicTicketFilterForm(request.POST, integration=integration)
        if form.is_valid():
            saved_filter.filter_data = form.cleaned_data
            saved_filter.name = request.POST.get('filter_name')
            saved_filter.save()
            return redirect('filter', integration_id=integration.id)
    
    form = DynamicTicketFilterForm(saved_filter.filter_data, integration=integration)
    return render(request, 'filters/update.html', {'form': form, 'integration': integration, 'saved_filter': saved_filter})


def delete_filter(request, filter_id):
    saved_filter = get_object_or_404(SavedFilter, id=filter_id, user=request.user)
    integration_id = saved_filter.integration.id
    if request.method == 'POST':
        saved_filter.delete()
        return redirect('filter', integration_id=integration_id)
    return render(request, 'filters/delete.html', {'saved_filter': saved_filter})

def view_filter(request, filter_id):
    saved_filter = get_object_or_404(SavedFilter, id=filter_id, user=request.user)
    integration = saved_filter.integration
    form = DynamicTicketFilterForm(saved_filter.filter_data, integration=integration)
    return render(request, 'filters/view.html', {'form': form, 'integration': integration, 'saved_filter': saved_filter})