import pytest
from apps.tickets.models.integrations import Integration, SavedFilter
from django.urls import reverse
from apps.customer_accounts.test_utils import *
from apps.test_utils import *
from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant
from django.contrib.auth import get_user_model
    
User = get_user_model() 
@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_tickets_integrations_acc')
def test_ticket_list_filter(client, account_fixture, integration_fixture):
    set_current_tenant(account_fixture)
    
    integration_id = integration_fixture.id
    url = reverse('filter', args=[integration_id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context
    assert 'tickets' in response.context
    tickets = response.context['tickets']
    
    assert len(tickets) == 0  # Expecting empty form, so no tickets yet

@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_tickets_integrations_acc')
def test_ticket_list_apply_filter(client, account_fixture, integration_fixture, logged_in_client):
    set_current_tenant(account_fixture)
    client = logged_in_client
    
    url = reverse('filter', args=[integration_fixture.id])
    response = client.post(url, {
        'id': 1,
    })

    assert response.status_code == 200
    assert 'tickets' in response.context
    tickets = response.context['tickets']
    
    # Assuming the filtered tickets contain 'Test Subject'
    assert any(ticket.id == 1 for ticket in tickets)

@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_tickets_integrations_acc')
def test_create_filter(client, account_fixture, freshdesk_integration_fixture,logged_in_client,new_user_fixture):
    set_current_tenant(account_fixture)
    client = logged_in_client
    client.force_login(new_user_fixture)
    integration_id = freshdesk_integration_fixture.id
    url = reverse('create_filter', args=[integration_id])
    response = client.post(url, {
        'id': 1,
        'filter_name': 'Test Filter 2'
    })

    assert response.status_code == 302
    assert response.url == reverse('filter', args=[integration_id])

    # Verify the filter is created in the database
    saved_filter = SavedFilter.objects.get(name='Test Filter 2')
    assert saved_filter
    assert saved_filter.filter_data['id'] == 1

@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_tickets_integrations_acc')
def test_ticket_list_load_saved_filter(client, account_fixture,user_fixture,freshdesk_integration_fixture, logged_in_client):
    user = user_fixture
    set_current_tenant(account_fixture)
    client = logged_in_client
    client.force_login(user_fixture)
    
    saved_filter = SavedFilter.objects.create(
        user=user,
        integration=freshdesk_integration_fixture,
        filter_data={'id': '1'},
        name='Test Filter'
    )
    
    url = reverse('filter', args=[freshdesk_integration_fixture.id])
    response = client.post(url, {
        'filter_id': saved_filter.id,
    })

    assert response.status_code == 200
    assert 'tickets' in response.context
    tickets = response.context['tickets']
    
    # Assuming the saved filter returns tickets with 'Test Subject'
    assert any(ticket.id == 1 for ticket in tickets)
    
@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_tickets_integrations_acc')
def test_update_filter(client, account_fixture, user_fixture, freshdesk_integration_fixture, logged_in_client):
    user = user_fixture
    set_current_tenant(account_fixture)
    client = logged_in_client
    client.force_login(user_fixture)
    
    saved_filter = SavedFilter.objects.create(
        user=user,
        integration=freshdesk_integration_fixture,
        filter_data={'subject': 'Test Subject'},
        name='Test Filter'
    )
    
    url = reverse('update_filter', args=[saved_filter.id])
    response = client.post(url, {
        'subject': 'Updated Subject',
        'filter_name': 'Updated Filter Name'
    })

    assert response.status_code == 302
    assert response.url == reverse('filter', args=[freshdesk_integration_fixture.id])

    # Verify the filter is updated in the database
    saved_filter.refresh_from_db()
    assert saved_filter.name == 'Updated Filter Name'
    assert saved_filter.filter_data['subject'] == 'Updated Subject'

@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_tickets_integrations_acc')
def test_delete_filter(client, account_fixture, user_fixture, freshdesk_integration_fixture, logged_in_client):
    user = user_fixture
    set_current_tenant(account_fixture)
    client = logged_in_client
    client.force_login(user_fixture)
    
    saved_filter = SavedFilter.objects.create(
        user=user,
        integration=freshdesk_integration_fixture,
        filter_data={'subject': 'Test Subject'},
        name='Test Filter'
    )
    
    url = reverse('delete_filter', args=[saved_filter.id])
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('filter', args=[freshdesk_integration_fixture.id])

    # Verify the filter is deleted from the database
    with pytest.raises(SavedFilter.DoesNotExist):
        SavedFilter.objects.get(id=saved_filter.id)

@pytest.mark.django_db
@pytest.mark.usefixtures('filterable_fields_yaml', 'django_db_setup_tickets_integrations_acc')
def test_view_filter(client, account_fixture, user_fixture, freshdesk_integration_fixture, logged_in_client):
    user = user_fixture
    set_current_tenant(account_fixture)
    client = logged_in_client
    client.force_login(user_fixture)
    
    saved_filter = SavedFilter.objects.create(
        user=user,
        integration=freshdesk_integration_fixture,
        filter_data={'id': 1},
        name='Test Filter'
    )
    
    url = reverse('view_filter', args=[saved_filter.id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context
    assert 'integration' in response.context
    assert 'saved_filter' in response.context
    form = response.context['form']
    
    assert form.data['id'] == 1
    assert response.context['saved_filter'].name == 'Test Filter'