from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import AssignmentRule, TicketAssignment
from ..forms import AssignmentRuleForm, TicketAssignmentForm

@login_required
def assignment_rule_list(request):
    rules = AssignmentRule.objects.all()
    return render(request, 'assignments/list_rules.html', {'rules': rules})

@login_required
def create_assignment_rule(request):
    if request.method == 'POST':
        form = AssignmentRuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment rule created successfully.')
            return redirect('assignment_rule_list')
    else:
        form = AssignmentRuleForm()

    return render(request, 'assignments/create_rule.html', {'form': form})

@login_required
def create_ticket_assignment(request):
    if request.method == 'POST':
        form = TicketAssignmentForm(request.POST)
        if form.is_valid():
            ticket_assignment = form.save(commit=False)
            ticket_assignment.account_id = request.user.id
            ticket_assignment.save()
            messages.success(request, 'Ticket assignment created successfully.')
            return redirect('ticket_assignment_list')
        else:
            print('Form submission failed:', form.errors)  # Print form errors to console
    else:
        form = TicketAssignmentForm()

    return render(request, 'assignments/create_assignments.html', {'form': form})
# ADDED BY SMARTDEV-CODE
@login_required
def create_ticket_assignment_add_filter(request):
    if request.method == 'POST':
        form = TicketAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket assignment created successfully.')
            return redirect('ticket_assignment_list')
    else:
        form = TicketAssignmentForm()

    return render(request, 'assignments/create_assignments_add_filter.html', {'form': form})

@login_required
def ticket_assignment_list(request):
    assignments = TicketAssignment.objects.all()
    return render(request, 'assignments/list_assignments.html', {'assignments': assignments})

def ticket_assignment_dashboard(request):
        #TODO: for now, there's no difference between the assignment lsit and dashboard
        return redirect('ticket-assignments/ticket_assignment_list' ) 