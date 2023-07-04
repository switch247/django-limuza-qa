from django.shortcuts import render, redirect, get_object_or_404
from apps.reviews.models import TicketReview, ReviewCategory, Scorecard, Category
from apps.tickets.models import Ticket
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages
from ..forms import *
import logging

User = get_user_model()

# Initialize logger
logger = logging.getLogger(__name__)

@login_required
def create_ticket_review(request, ticket_id):
    """
    Creates a draft review for the specified ticket and redirects to the review show page.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    scorecard = Scorecard.objects.first()  # Default scorecard

    if not scorecard:
        logger.error('No scorecard found. Please add a scorecard first.')
        raise Exception('Add a scorecard first!')

    review = TicketReview.objects.create(
        ticket=ticket,
        scorecard=scorecard,
        reviewer=request.user,
        agent=ticket.agent,
        date=timezone.now(),
        comments='',
        draft=True  # Initially set to draft
    )
    return redirect('show_review', review_id=review.id)

@login_required
def show_review(request, review_id):
    """
    Displays the review details.
    This method should check if the review exists; otherwise, it should throw an error.

    It should send through the ticket information as well as a form with either:
    - Check if there are any review categories and send those.
    - If not, send the scorecard categories for the scorecard linked to the review.
    Only one of the two should be sent, and nil for the other.
    """
    review = get_object_or_404(TicketReview, id=review_id)
    ticket = review.ticket
    conversations = ticket.conversations.all()
    cat = review.get_categories()
    form = ReviewForm(review_data=cat, instance=review)
    scorecard_form = SelectScorecardForm()
    context = {
        'review': review,
        'ticket': ticket,
        'conversations': conversations,
        'form': form,
        'scorecard_form':scorecard_form,
        'scorecards': Scorecard.objects.all(),
        'scorecard_categories': cat,
        'review_categories': cat,
    }
    return render(request, 'reviews/show_review.html', context)


@login_required
def change_scorecard(request, review_id):
    # check if post and if it is a scorecard update
    # if so, update the scorecard and return the div
    if request.method != 'POST' and request.POST.get('select_scorecard') != 'true':
        raise Exception('boo! What are you doing?')
    review = get_object_or_404(TicketReview, id=review_id)
    new_scorecard = get_object_or_404(Scorecard, id=request.POST.get('scorecard'))
    review.update_scorecard(new_scorecard)
    scorecard_categories = review.get_categories()
    form = ReviewForm(review_data=scorecard_categories, instance=review)
    scorecard_form = SelectScorecardForm()
    context = {
        'review': review,
        'form': form,
        'scorecard_form':scorecard_form,
        'scorecards': Scorecard.objects.all(),
        'scorecard_categories': scorecard_categories,
        'review_categories': scorecard_categories,
    }
    return render(request, 'reviews/_review_view.html', context)


@login_required
def save_review(request, review_id):
    """
    Saves or updates the review with the data submitted via POST request.
    """
    if request.method != 'POST':
        raise Exception('Add a scorecard first!')


    review = get_object_or_404(TicketReview, id=review_id)
    scorecard_categories = review.scorecard.scorecard_categories.all()
    review_categories = {rc.scorecard_category.id: rc for rc in review.review_categories.all()}

    form = ReviewForm(request.POST, review_data=[sc.to_json() for sc in scorecard_categories], instance=review)
    if form.is_valid():
        review = form.save(commit=False)
        review.draft = False  # Set draft to False on save
        scorecard_id = request.POST.get('scorecard_id')
        if scorecard_id:
            scorecard = get_object_or_404(Scorecard, id=scorecard_id)
            review.update_scored(scorecard)
            scorecard_categories = review.get_categories()
        review.save()
        for sc_category in scorecard_categories:
            field_name = f'category_{sc_category.category.id}'
            score = form.cleaned_data.get(field_name)
            review_category, created = ReviewCategory.objects.get_or_create(review=review, scorecard_category=sc_category)
            review_category.score = score
            review_category.save()
        messages.success(request, 'Review saved successfully.')
        return redirect('reviews/show_review', review_id=review.id)
    
    context = {
        'review': review,
        'ticket': review.ticket,
        'conversations': review.ticket.conversations.all(),
        'form': form,
        'scorecards': Scorecard.objects.all(),
    }
    return render(request, 'show_review.html', context)

@login_required
def delete_review(request, review_id):
    """
    Deletes the specified review and redirects to the review list page.
    """
    review = get_object_or_404(TicketReview, id=review_id)
    review.delete()
    messages.success(request, 'Review deleted successfully.')
    return redirect('list_reviews')

@login_required
def list_reviews(request):
    """
    Retrieves a list of all TicketReviews and renders them in the 'list_reviews.html' template.
    """
    reviews = TicketReview.objects.all()  # TODO: this Assumes you only want to list TicketReviews
    return render(request, 'reviews/list_reviews.html', {'reviews': reviews})


@login_required 
def show_dashboard(request):
    """
    Displays the dashboard. Dummy for now. TODO dummy.
    """
    donut_data = {
    'title': 'Reviews Completed',
    'info1Heading': "Channel Performance - Review Sentiment",
    'info1paragraph': "This chart displays the distribution of reviews across different channels, categorized by sentiment (Good, Bad, Great). It helps identify which channels are performing well and which need improvement.",
    'info2Heading': "Sentiment Calculation",
    'info2paragraph': "For each channel, reviews are categorized into Good, Bad, and Great. The segments show the volume of each sentiment, providing insights into customer satisfaction and areas for potential enhancement.",
    'further_info_link': 'Breakdown',
    'filter_a' : 'Calls',
    'filter_b' : 'Emails',
    'filter_c' : 'Chats',
    }
    area_data = {
    'title_value': '78%',
    'title': 'Avg QA Score this week',
    'further_info_link': 'Score Breakdowns',
    'improvement_value': '12%'
    }
    coverage_data = {
    'title_value': '78%',
    'title': 'Avg QA Score this week',
    'further_info_link': 'Score Breakdowns',
    'improvement_value': '12%'
    }
    return render(request, 'dashboard/index.html', {'chart_data': donut_data,'area_data': area_data})

@login_required 
def show_agent_dashboard(request):
    """
    Displays the dashboard. Dummy for now. TODO dummy.
    """
    donut_data = {
    'title': 'Reviews Completed',
    'info1Heading': "Channel Performance - Review Sentiment",
    'info1paragraph': "This chart displays the distribution of reviews across different channels, categorized by sentiment (Good, Bad, Great). It helps identify which channels are performing well and which need improvement.",
    'info2Heading': "Sentiment Calculation",
    'info2paragraph': "For each channel, reviews are categorized into Good, Bad, and Great. The segments show the volume of each sentiment, providing insights into customer satisfaction and areas for potential enhancement.",
    'further_info_link': 'Breakdown',
    'filter_a' : 'Calls',
    'filter_b' : 'Emails',
    'filter_c' : 'Chats',
    }
    area_data = {
    'title_value': '78%',
    'title': 'Avg QA Score this week',
    'further_info_link': 'Score Breakdowns',
    'improvement_value': '12%'
    }
    coverage_data = {
    'title_value': '78%',
    'title': 'Avg QA Score this week',
    'further_info_link': 'Score Breakdowns',
    'improvement_value': '12%'
    }
    return render(request, 'dashboard/agent_index.html', {'chart_data': donut_data,'area_data': area_data})