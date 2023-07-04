from django.shortcuts import render, redirect, get_object_or_404
from apps.reviews.models import TicketReview, ReviewCategory, Category
from django.contrib.auth.decorators import login_required
from apps.reviews.models import TicketReview, Scorecard
from apps.tickets.models import Ticket
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from ..forms import *
from ..models import *
from django.db import IntegrityError

User = get_user_model()

@login_required
def list_scorecards(request):
    scorecards = Scorecard.objects.all()
    return render(request, 'scorecards/list_scorecards.html', {'scorecards': scorecards})

@login_required
def create_scorecard(request):
    if request.method == 'POST':
        form = ScorecardForm(request.POST)
        if form.is_valid():
            try:
                scorecard = form.save(commit=False)
                scorecard.created_by = request.user
                scorecard.save()

                selected_categories = form.cleaned_data['categories']
                for category in selected_categories:
                    weight = request.POST.get(f'weight_{category.id}', 1.0)  # Default weight if not specified
                    ScorecardCategory.objects.create(
                        scorecard=scorecard,
                        category=category,
                        weighting=weight
                    )
                messages.success(request, 'Scorecard created successfully.')
                return redirect('list_scorecards')
            except IntegrityError:
                messages.error(request, 'There was an error creating the scorecard. Please ensure all fields are filled correctly.')
        else:
            messages.error(request, 'There was an error with the form. Please check the fields and try again.')
    else:
        form = ScorecardForm()

    context = {
        'form': form,
    }
    return render(request, 'scorecards/create_scorecard.html', context)




@login_required
def view_scorecard(request, scorecard_id):
    scorecard = get_object_or_404(Scorecard, id=scorecard_id)
    scorecard_categories = scorecard.get_categories()
    return render(request, 'scorecards/view_scorecard.html', {'scorecard': scorecard, 'scorecard_categories': scorecard_categories})