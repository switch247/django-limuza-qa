import pytest
from django.contrib.auth import get_user_model
from apps.reviews.models import Scorecard, Category, ScorecardCategory, Review, TicketReview, ConversationReview, ReviewCategory
from apps.tickets.models import Ticket, Conversation, Integration
from apps.test_utils import *
from django.urls import reverse
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant


User = get_user_model()

@pytest.mark.django_db
def test_save_review(admin_client, scorecard, category_tone, category_spelling, ticket):
    # Create another scorecard to test scorecard change
    new_scorecard = Scorecard.objects.create(
        name='New Scorecard', created_by=ticket.agent, account_id='account2'
    )
    ScorecardCategory.objects.create(scorecard=new_scorecard, category=category_tone, weighting=1.0)
    ScorecardCategory.objects.create(scorecard=new_scorecard, category=category_spelling, weighting=1.0)
    
    review = TicketReview.objects.create(
        ticket=ticket,
        scorecard=scorecard,
        reviewer=ticket.agent,
        agent=ticket.agent,
        comments='Initial review comments'
    )

    
    data = {
        'review_id': review.id,
        'scorecard_id': new_scorecard.id,
        'select_scorecard': 'Change Scorecard',
        'comments': 'Updated review comments',
    }

    url = reverse('save_review', args=[review.id])
    response = admin_client.post(url, data)
    
    review.refresh_from_db()
    assert response.status_code == 302
    assert review.scorecard == new_scorecard
    assert review.comments == 'Updated review comments'

@pytest.mark.django_db
def test_get_review_data(admin_user, scorecard, ticket):
    # Create scorecard categories
    category_tone = Category.objects.create(name='Tone', scale='3_point', allow_na=True)
    category_spelling = Category.objects.create(name='Spelling', scale='binary', allow_na=False)
    scorecard_category_tone = ScorecardCategory.objects.create(scorecard=scorecard, category=category_tone, weighting=1.5)
    scorecard_category_spelling = ScorecardCategory.objects.create(scorecard=scorecard, category=category_spelling, weighting=1.0)

    # Create a ticket review without review categories
    review = TicketReview.objects.create(
        ticket=ticket,
        scorecard=scorecard,
        reviewer=admin_user,
        agent=admin_user,
        comments='Test ticket review comments'
    )

    # Test get_review_data when there are no review categories
    review_categories = review.get_categories()
    #check type 
    
    assert isinstance(review_categories[0],ScorecardCategory)
    #the above checks the wrong thing
    assert list(review_categories) == [scorecard_category_tone, scorecard_category_spelling]
    #assert review_categories is None

    # Create review categories
    review_category_tone = ReviewCategory.objects.create(review=review, scorecard_category=scorecard_category_tone, score=2)
    review_category_spelling = ReviewCategory.objects.create(review=review, scorecard_category=scorecard_category_spelling, score=1)

    # Test get_review_data when there are review categories
    review_data, scorecard_categories, review_categories = review.get_review_data()
    assert review_data == [review_category_tone.to_json(), review_category_spelling.to_json()]
    assert scorecard_categories is None
    assert list(review_categories) == [review_category_tone, review_category_spelling]
