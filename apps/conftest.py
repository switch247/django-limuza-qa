import json
import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from apps.customer_accounts.middleware import MultitenantMiddleware
from django.core.management import call_command
from apps.customer_accounts.models import CustomerAccount, Workspace
from apps.tickets.models.integrations import Integration, FreshdeskIntegration
from apps.tickets.models import Ticket, Conversation
from django.test import RequestFactory
from apps.reviews.models import Scorecard, Category, ScorecardCategory, Review, TicketReview, ConversationReview, ReviewCategory
import yaml
# Import conftest from apps/accounts/tests
from apps.customer_accounts.tests.fixtures import *
User = get_user_model()

# @pytest.fixture(scope='session')
# def django_db_setup_accounts(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'apps/accounts/fixtures/accounts.json')
        


# @pytest.fixture(scope='session')
# def django_db_setup_tickets(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'apps/tickets/fixtures/tickets.json')
        
# @pytest.fixture(scope='session')
# def django_db_setup_reviews(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'apps/reviews/fixtures/reviews.json')
        
# @pytest.fixture(scope='session')
# def django_db_setup_integrations_and_acc(django_db_setup_accounts, django_db_setup_tickets):
#     pass  # The other fixtures will be executed automatically
        
# @pytest.fixture(scope='session')
# def django_db_setup_tickets_integrations_acc(django_db_setup_accounts,django_db_setup_tickets):
#     pass  # The other fixtures will be executed automatically           

# @pytest.fixture(scope='session')
# def django_db_setup_reviews_tickets_integrations_acc(django_db_setup_accounts, django_db_setup_tickets,django_db_setup_reviews):
#     pass  # The other fixtures will be executed automatically      
# @pytest.fixture
# def user_fixture():
#     return User.objects.first()

# @pytest.fixture
# def admin_user_fixture():
#     return User.objects.first()
# @pytest.fixture
# def account_fixture():
#     return Account.objects.first()

# @pytest.fixture
# def workspace_fixture():
#     return Workspace.objects.first()


# @pytest.fixture
# def integration_fixture():
#     return Integration.objects.first()

# @pytest.fixture
# def conversation_fixture():
#     return Conversation.objects.first()

# @pytest.fixture
# def ticket_fixture():
#     return Ticket.objects.first()

# @pytest.fixture
# def freshdesk_integration_fixture():
#     return FreshdeskIntegration.objects.first()

# @pytest.fixture
# def category_fixture():
#     return Category.objects.first()

# @pytest.fixture
# def tone_category_fixture():
#     return Category.objects.filter(name= "Tone").first()

# @pytest.fixture
# def spelling_category_fixture():
#     return Category.objects.filter(name= "Spelling").first()

# @pytest.fixture
# def scorecard_fixture():
#     return Scorecard.objects.all()[1]

# @pytest.fixture
# def scorecard_category_fixture():
#     return ScorecardCategory.objects.first()

# @pytest.fixture
# def scorecard_tone_category_fixture(tone_category_fixture):
#     return ScorecardCategory.objects.filter(category=tone_category_fixture).first()

# @pytest.fixture
# def scorecard_spelling_category_fixture(spelling_category_fixture):
#     return ScorecardCategory.objects.filter(category=spelling_category_fixture).first()

# @pytest.fixture
# def review_spelling_category_fixture():
#     return ReviewCategory.objects.first()

# @pytest.fixture
# def review_tone_category_fixture():
#     return ReviewCategory.objects.all()[1]

# @pytest.fixture
# def ticket_review_fixture():
#     return TicketReview.objects.first()

# @pytest.fixture
# def new_user_fixture():
#     u = User.objects.create(
#             username='testuser2',
#             email='testuser@test.com',
#             external_id=1234,
#             password='password'  # or use a more secure way to set passwords
#         )
#     return u

# @pytest.fixture
# def conversation_review_fixture():
#     return ConversationReview.objects.first()


# @pytest.fixture
# def middleware():
#     def get_response(request):
#         return None
#     return MultitenantMiddleware(get_response)

# @pytest.fixture
# def request_factory():
#     return RequestFactory()
    
# @pytest.fixture
# def filterable_fields_yaml():
#     path = 'apps/tickets/filters/FreshdeskIntegration.yaml'
#     with open(path, 'r') as file:
#         data = yaml.safe_load(file)
#     return data


# @pytest.fixture
# def logged_in_client(client, new_user_fixture):
#     user = new_user_fixture
#     client.login(username=user.username, password='password')
#     return client

