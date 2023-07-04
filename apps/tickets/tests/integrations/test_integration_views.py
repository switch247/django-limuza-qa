# import pytest
# from django.contrib.auth import get_user_model
# from ...models import Integration, Ticket
# from apps.customer_accounts.test_utils import *
# from apps.test_utils import *
# from apps.tickets.services import *
# import os
# import json
# from django_multitenant.utils import set_current_tenant, unset_current_tenant, get_current_tenant

# user = get_user_model()

# @pytest.mark.django_db
# def test_setup_new_crm_integration():
#     """
#     Given an admin user with appropriate permissions,
#     When the admin sets up a new CRM integration,
#     Then a new integration record is created in the system,
#     And the integration details are stored in the database,
#     And the integration is associated with the correct workspace.
#     """
#     # Given
#     user,account, workspace = create_admin_user_and_account(admin = True)
#     set_current_tenant(account)
#     # When
#     dummy_integration_data = {
#     "name": "Test CRM Integration",
#     "type": "freshdesk",
#     "integration_key": "fake_integration_key",
#     "active": True,
#     "details": {
#         "api_key": "fake_api_key",
#         "url": "https://api.fake-crm.com"
#         }
#     }
#     integration = setup_crm_integration(user, workspace, dummy_integration_data)
    
#     # Then
#     assert integration.account == account
#     assert Integration.objects.filter(id=integration.id).exists()
#     assert integration.workspace == workspace
#     assert integration.details == dummy_integration_data['details']
#     unset_current_tenant()



# # @pytest.mark.django_db
# # def test_fetch_new_tickets_from_crm():
# #     """
# #     Given a valid and active CRM integration,
# #     And there are new tickets available in CRM,
# #     When the background job runs to fetch new tickets,
# #     Then the new tickets are retrieved from CRM,
# #     And the tickets are processed and stored in the system,
# #     And each ticket's original data is stored in the ticket_data field,
# #     And each ticket is associated with the correct integration.
# #     """
# #     # Given
# #     user, workspace = create_admin_user_and_account(admin=True)
# #     integration_data = {
# #         "name": "Test CRM Integration",
# #         "type": "freshdesk",
# #         "integration_key": "fake_integration_key",
# #         "active": True,
# #         "details": {
# #             "api_key": "fake_api_key",
# #             "url": "https://api.fake-crm.com"
# #         }
# #     }
# #     integration = setup_crm_integration(user, workspace, integration_data)

# #     # Mocking the API response for Freshdesk
# #     mock_tickets = [
# #         {
# #             "id": "123",
# #             "subject": "Test Ticket 1",
# #             "status": "open",
# #             "created_at": "2024-05-19T12:37:15Z",
# #             "updated_at": "2024-05-20T12:37:15Z",
# #             "description": "HTML description",
# #             "description_text": "Text description",
# #             "conversations": [
# #                 {"body": "HTML conversation", "body_text": "Text conversation"}
# #             ]
# #         },
# #         {
# #             "id": "124",
# #             "subject": "Test Ticket 2",
# #             "status": "closed",
# #             "created_at": "2024-05-19T12:37:15Z",
# #             "updated_at": "2024-05-20T12:37:15Z",
# #             "description": "HTML description 2",
# #             "description_text": "Text description 2",
# #             "conversations": [
# #                 {"body": "HTML conversation 2", "body_text": "Text conversation 2"}
# #             ]
# #         }
# #     ]

# #     # Mock the fetch_tickets method
# #     with patch.object(FreshdeskIntegration, 'fetch_tickets', return_value=mock_tickets):
# #         new_tickets = integration.fetch_tickets()

# #         # Ensure the tickets were fetched
# #         assert len(new_tickets) > 0

# #         # When
# #         for ticket_data in new_tickets:
# #             ticket = Ticket.objects.create(
# #                 external_id=ticket_data['id'],
# #                 subject=ticket_data['subject'],
# #                 created_at=datetime.strptime(ticket_data['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
# #                 status=ticket_data['status'],
# #                 ticket_data=ticket_data,
# #                 html_ticket=ticket_data['conversations'][0]['body'],
# #                 text_ticket=ticket_data['conversations'][0]['body_text'],
# #                 integration=integration
# #             )
# #             # Then
# #             assert Ticket.objects.filter(id=ticket.id).exists()
# #             assert ticket.ticket_data is not None
# #             assert ticket.integration == integration

































# # @pytest.mark.django_db
# # def test_delete_integration(admin_user):
# #     """
# #     Given a valid and active CRM integration,
# #     When an admin user deletes the integration,
# #     Then the integration record is removed from the system,
# #     And the association with the workspace is removed,
# #     And no new tickets are fetched from the deleted integration,
# #     And historical tickets remain in the system.
# #     """
# #     # Given
# #     integration = create_test_integration(active=True)
# #     workspace = integration.workspace

# #     # When
# #     delete_integration(admin_user, integration)

# #     # Then
# #     assert not Integration.objects.filter(id=integration.id).exists()
# #     assert integration.workspace != workspace
# #     assert not fetch_tickets_from_crm(integration)  # This should not fetch any new tickets
# #     assert historical_tickets_exist(workspace)  # This function checks if historical tickets still exist

# # @pytest.mark.django_db
# # def test_update_integration_details(admin_user):
# #     """
# #     Given a valid and active CRM integration,
# #     When an admin user updates the integration details,
# #     Then the updated details are saved in the system,
# #     And the integration record is updated in the database,
# #     And the integration continues to function with the new details.
# #     """
# #     # Given
# #     integration = create_test_integration(active=True)
# #     new_details = {"api_key": "new_api_key"}

# #     # When
# #     update_integration_details(admin_user, integration, new_details)

# #     # Then
# #     updated_integration = Integration.objects.get(id=integration.id)
# #     assert updated_integration.details["api_key"] == new_details["api_key"]
# #     assert integration_functioning(updated_integration)

# # @pytest.mark.django_db
# # def test_disable_integration(admin_user):
# #     """
# #     Given a valid and active CRM integration,
# #     When an admin user disables the integration,
# #     Then the integration status is set to inactive,
# #     And no new tickets are fetched from the integration,
# #     And existing tickets from the integration remain in the system.
# #     """
# #     # Given
# #     integration = create_test_integration(active=True)

# #     # When
# #     disable_integration(admin_user, integration)

# #     # Then
# #     assert not integration.active
# #     assert not fetch_tickets_from_crm(integration)  # This should not fetch any new tickets
# #     assert existing_tickets_remain(integration)

# # @pytest.mark.django_db
# # def test_disable_integration(admin_user):
# #     """
# #     Given a valid and active CRM integration,
# #     When an admin user disables the integration,
# #     Then the integration status is set to inactive,
# #     And no new tickets are fetched from the integration,
# #     And existing tickets from the integration remain in the system.
# #     """
# #     # Given
# #     integration = create_test_integration(active=True)

# #     # When
# #     disable_integration(admin_user, integration)

# #     # Then
# #     assert not integration.active
# #     assert not fetch_tickets_from_crm(integration)  # This should not fetch any new tickets
# #     assert existing_tickets_remain(integration)

# # @pytest.mark.django_db
# # def test_enable_integration(admin_user):
# #     """
# #     Given a valid but inactive CRM integration,
# #     When an admin user enables the integration,
# #     Then the integration status is set to active,
# #     And new tickets can be fetched from the integration,
# #     And the integration resumes normal operation.
# #     """
# #     # Given
# #     integration = create_test_integration(active=False)

# #     # When
# #     enable_integration(admin_user, integration)

# #     # Then
# #     assert integration.active
# #     assert fetch_tickets_from_crm(integration)  # This should fetch new tickets

# # @pytest.mark.django_db
# # def test_error_handling_during_ticket_fetching():
# #     """
# #     Given a valid and active CRM integration,
# #     And there is a temporary issue with the CRM API,
# #     When the background job runs to fetch new tickets,
# #     Then an error is logged in the system,
# #     And the job retries fetching tickets after a specified interval,
# #     And no duplicate tickets are created if the fetching is retried successfully.
# #     """
# #     # Given
# #     integration = create_test_integration(active=True)

# #     # Mock a temporary CRM API issue
# #     mock_crm_api_issue()

# #     # When
# #     fetch_tickets_with_error_handling(integration)

# #     # Then
# #     assert error_logged("Temporary CRM API issue")
# #     assert fetch_tickets_from_crm(integration)  # This should eventually fetch new tickets
# #     assert no_duplicate_tickets(integration)
