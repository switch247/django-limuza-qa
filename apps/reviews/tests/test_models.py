import pytest
from django.contrib.auth import get_user_model
from apps.reviews.models import Scorecard, Category, ScorecardCategory, Review, TicketReview, ConversationReview, ReviewCategory
from apps.tickets.models import Ticket, Conversation, Integration
from apps.test_utils import *
from django.urls import reverse
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant


User = get_user_model()

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username='admin', password='password')
    user.is_staff = True
    user.save()
    return user


@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_category_to_json(category_fixture):
    expected_json = {
        'id': category_fixture.id,
        'name': category_fixture.name,
        'scale': category_fixture.scale,
        'allow_na': category_fixture.allow_na,
    }
    assert category_fixture.to_json() == expected_json

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_scorecard_to_json(scorecard_fixture):
    scorecard = scorecard_fixture
    expected_json = {
        'id': scorecard.id,
        'name': scorecard.name,
    }
    assert scorecard.to_json() == expected_json

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_scorecard_category_to_json(scorecard_category_fixture):
    scorecard_category_tone = scorecard_category_fixture
    expected_json = {
        'id': scorecard_category_tone.id,
        'scorecard': scorecard_category_tone.scorecard.to_json(),
        'category': scorecard_category_tone.category.to_json(),
        'weighting': scorecard_category_tone.weighting,
    }
    assert scorecard_category_tone.to_json() == expected_json

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_review_category_to_json(review_spelling_category_fixture):
    sc = review_spelling_category_fixture.scorecard_category
    expected_json = {
        'id': review_spelling_category_fixture.id,
        'score': review_spelling_category_fixture.score,
        'na': review_spelling_category_fixture.na,
        'scorecard_category': sc.to_json()
    }
    assert review_spelling_category_fixture.to_json() == expected_json

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_scorecard_get_categories(scorecard_fixture, scorecard_tone_category_fixture, scorecard_spelling_category_fixture):
    categories = scorecard_fixture.get_categories()
    assert categories.count() == 2
    assert scorecard_tone_category_fixture in categories #TODO fix fixture
    assert scorecard_spelling_category_fixture in categories

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_review_get_categories(ticket_review_fixture, review_spelling_category_fixture, review_tone_category_fixture):
    # Test when there are review categories
    categories = ticket_review_fixture.get_categories()
    assert categories.count() == 2
    assert review_spelling_category_fixture in categories

    # Test when there are no review categories
    review_spelling_category_fixture.delete()
    categories = ticket_review_fixture.get_categories()
    assert categories.count() == 1
    assert review_tone_category_fixture in categories

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_create_scorecard_with_categories(account_fixture, scorecard_fixture, tone_category_fixture, spelling_category_fixture):
    set_current_tenant(account_fixture)
    ScorecardCategory.objects.filter(scorecard=scorecard_fixture).delete()
    c1 = Category.objects.create(name='Solution', scale='3_point', allow_na=True)
    c2 = Category.objects.create(name='Workaround', scale='3_point', allow_na=True)
    ScorecardCategory.objects.create(scorecard=scorecard_fixture, category=c1, weighting=1.5)
    ScorecardCategory.objects.create(scorecard=scorecard_fixture, category=c2, weighting=1.0)
    unset_current_tenant()
    assert ScorecardCategory.objects.filter(scorecard=scorecard_fixture).count() == 2

@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup_reviews_tickets_integrations_acc')
def test_create_ticket_review(account_fixture,scorecard_fixture, tone_category_fixture, spelling_category_fixture, ticket_fixture):
    set_current_tenant(account_fixture)
    ScorecardCategory.objects.filter(scorecard=scorecard_fixture).delete()

    reviewer = User.objects.create_user(username='reviewer', password='password')
    agent = User.objects.create_user(username='agent', password='password')
    c1 = Category.objects.create(name='Solution', scale='3_point', allow_na=True)
    c2 = Category.objects.create(name='Workaround', scale='3_point', allow_na=True)
    sc1 = ScorecardCategory.objects.create(scorecard=scorecard_fixture, category=c1, weighting=1.5)
    sc2 = ScorecardCategory.objects.create(scorecard=scorecard_fixture, category=c2, weighting=1.0)

    review = TicketReview.objects.create(
        ticket=ticket_fixture,
        scorecard=scorecard_fixture,
        reviewer=reviewer,
        agent=agent,
        comments='Test ticket review comments'
    )
    
    ReviewCategory.objects.create(review=review, scorecard_category=sc1, score=2)
    ReviewCategory.objects.create(review=review, scorecard_category=sc2, score=1)
    unset_current_tenant()
    assert ScorecardCategory.objects.all().count() == 2
    assert TicketReview.objects.filter(id=review.id).exists()
    assert ReviewCategory.objects.filter(review=review).count() == 2
    assert ReviewCategory.objects.get(review=review, scorecard_category=sc1).score == 2
    assert ReviewCategory.objects.get(review=review, scorecard_category=sc2).score == 1

@pytest.mark.skip(reason="not implemented")
def test_create_conversation_review(account_fixture, scorecard_fixture, tone_category_fixture, spelling_category_fixture, conversation_fixture):
    reviewer = User.objects.create_user(username='reviewer', password='password')
    agent = User.objects.create_user(username='agent', password='password')
    
    ScorecardCategory.objects.create(scorecard=scorecard_fixture, category=category_tone, weighting=1.5)
    ScorecardCategory.objects.create(scorecard=scorecard_fixture, category=category_spelling, weighting=1.0)

    review = ConversationReview.objects.create(
        conversation=conversation_fixture,
        scorecard=scorecard_fixture,
        reviewer=reviewer,
        agent=agent,
        comments='Test conversation review comments'
    )
    
    ReviewCategory.objects.create(review=review, category=category_tone, score=2)
    ReviewCategory.objects.create(review=review, category=category_spelling, score=1)

    assert ConversationReview.objects.filter(conversation=conversation).exists()
    assert ReviewCategory.objects.filter(review=review).count() == 2
    assert ReviewCategory.objects.get(review=review, category=category_tone).score == 2
    assert ReviewCategory.objects.get(review=review, category=category_spelling).score == 1
