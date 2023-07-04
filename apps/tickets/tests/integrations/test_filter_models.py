import pytest
from datetime import datetime
from django import forms
from django.db.models import Q
from apps.tickets.models.integrations import Integration
from apps.tickets.models import Ticket, Conversation
from apps.tickets.forms import DynamicTicketFilterForm
from django.db import IntegrityError
from apps.customer_accounts.test_utils import *
from apps.test_utils import *
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant
import pytz
    
@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_integrations_and_acc')
def test_dynamic_ticket_filter_form_string(freshdesk_integration_fixture):
    form_data = {
        'subject': 'Test Subject',
        'subject_filter_type': 'contains'
    }
    form = DynamicTicketFilterForm(data=form_data, integration=freshdesk_integration_fixture)
    
    assert form.is_valid()
    filters = form.get_filters()
    
    expected_filters = Q(subject__icontains='Test Subject')
    assert filters == expected_filters


@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_integrations_and_acc')
def test_dynamic_ticket_filter_form_timestamp_between(freshdesk_integration_fixture):
    form_data = {
        'created_at': '2024-01-01',
        'created_at_end': '2024-01-31',
        'created_at_filter_type': 'between'
    }
    form = DynamicTicketFilterForm(data=form_data, integration=freshdesk_integration_fixture)
    
    assert form.is_valid()
    filters = form.get_filters()
    
    utc = pytz.UTC
    start_date = utc.localize(datetime.strptime('2024-01-01', '%Y-%m-%d'))
    end_date = utc.localize(datetime.strptime('2024-01-31', '%Y-%m-%d'))
    expected_filters = Q(created_at__range=(start_date, end_date))
    assert filters == expected_filters


@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_integrations_and_acc')
def test_dynamic_ticket_filter_form_timestamp_before(freshdesk_integration_fixture):
    form_data = {
        'created_at': '2024-01-01',
        'created_at_filter_type': 'before'
    }
    form = DynamicTicketFilterForm(data=form_data, integration=freshdesk_integration_fixture)
    
    assert form.is_valid()
    filters = form.get_filters()
    
    utc = pytz.UTC
    filter_date = utc.localize(datetime.strptime('2024-01-01', '%Y-%m-%d'))
    expected_filters = Q(created_at__lt=filter_date)
    assert filters == expected_filters


@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_integrations_and_acc')
def test_dynamic_ticket_filter_form_integer(freshdesk_integration_fixture):
    form_data = {
        'id': 1,
        'id_filter_type': 'is'
    }
    form = DynamicTicketFilterForm(data=form_data, integration=freshdesk_integration_fixture)
    
    assert form.is_valid()
    filters = form.get_filters()
    
    expected_filters = Q(id__exact=1)
    assert filters == expected_filters


@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_integrations_and_acc')
def test_dynamic_ticket_filter_form_array_contains_any(freshdesk_integration_fixture):
    form_data = {
        'tags': 'urgent,important',
        'tags_filter_type': 'contains_any'
    }
    form = DynamicTicketFilterForm(data=form_data, integration=freshdesk_integration_fixture)
    
    assert form.is_valid()
    filters = form.get_filters()
    
    expected_filters = Q(tags__overlap=['urgent', 'important'])
    assert filters == expected_filters


@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_integrations_and_acc')
def test_dynamic_ticket_filter_form_array_contains_all(freshdesk_integration_fixture):
    form_data = {
        'tags': 'urgent,important',
        'tags_filter_type': 'contains_all'
    }
    form = DynamicTicketFilterForm(data=form_data, integration=freshdesk_integration_fixture)
    
    assert form.is_valid()
    filters = form.get_filters()
    
    expected_filters = Q(tags__contains=['urgent', 'important'])
    assert filters == expected_filters


@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_integrations_and_acc')
def test_dynamic_ticket_filter_form_combined_filters(freshdesk_integration_fixture):
    form_data = {
        'subject': 'Test Subject',
        'subject_filter_type': 'contains',
        'created_at': '2024-01-01',
        'created_at_filter_type': 'after'
    }
    form = DynamicTicketFilterForm(data=form_data, integration=freshdesk_integration_fixture)
    
    assert form.is_valid()
    filters = form.get_filters()
    
    utc = pytz.UTC
    filter_date = utc.localize(datetime.strptime('2024-01-01', '%Y-%m-%d'))
    expected_filters = Q(subject__icontains='Test Subject') & Q(created_at__gt=filter_date)
    assert filters == expected_filters