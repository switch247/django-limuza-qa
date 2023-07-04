import pytest

from django.urls import reverse

from apps.customer_accounts import models
from apps.customer_accounts.tests import helpers
from apps.customer_accounts.tests.fixtures import *  # noqa


class TestWorkspacesListView:
    view_name = 'customer_accounts.workspaces_list'

    @pytest.mark.django_db
    def test_workspaces_list_view_requires_login(self, client):
        helpers.assert_view_requires_login(client, view_name=self.view_name)

    @pytest.mark.django_db
    def test_workspaces_list_view_renders_template(self, client, basic_test_user_and_account):
        test_user, _ = basic_test_user_and_account
        helpers.assert_view_renders_template(
            client, view_name=self.view_name,
            template_name='customer_accounts/view_workspaces.html',
            user=test_user
        )


class TestCreateWorkspaceView:
    view_name = 'customer_accounts.create_workspace'

    @pytest.mark.django_db
    def test_create_workspace_view_requires_login(self, client):
        helpers.assert_view_requires_login(client, view_name=self.view_name)

    @pytest.mark.django_db
    def test_create_workspace_view_renders_template(self, client, basic_test_user_and_account):
        test_user, _ = basic_test_user_and_account
        helpers.assert_view_renders_template(
            client, view_name=self.view_name,
            template_name='customer_accounts/create_workspace.html',
            user=test_user
        )

    @pytest.mark.django_db
    def test_create_workspace_view_post_method(
            self, client, basic_test_user_and_account):
        basic_test_user, customer_account = basic_test_user_and_account
        client.force_login(basic_test_user)

        post_data = {
            'name': 'Test Workspace',
            'account': customer_account,
            'description': 'A description of the new workspace'
        }
        response = client.post(reverse(self.view_name), post_data)
        assert response.status_code == 302
        assert models.Workspace.objects.filter(name='Test Workspace').exists()


class TestEditWorkspaceView:
    view_name = 'customer_accounts.edit_workspace'

    @pytest.mark.django_db
    def test_edit_workspace_view_requires_login(self, client, workspace_for_test_user):
        helpers.assert_view_requires_login(
            client, view_name=self.view_name,
            params_dict={'workspace_id': workspace_for_test_user.id}
        )

    @pytest.mark.django_db
    def test_edit_workspace_view_renders_template(self, client, basic_test_user_and_account, workspace_for_test_user):
        test_user, customer_account = basic_test_user_and_account
        helpers.assert_view_renders_template(
            client, view_name=self.view_name,
            template_name='customer_accounts/edit_workspaces.html',
            params_dict={'workspace_id': workspace_for_test_user.id},
            user=test_user
        )

    @pytest.mark.django_db
    def test_edit_workspace_view_post_method(
            self, client, basic_test_user_and_account, workspace_for_test_user):
        basic_test_user, customer_account = basic_test_user_and_account
        client.force_login(basic_test_user)
        post_data = {
            'name': 'Updated Workspace',
            'account': customer_account,
            'description': 'Updated description'
        }
        response = client.post(
            reverse(self.view_name, kwargs={'workspace_id': workspace_for_test_user.id}),
            post_data
        )
        assert response.status_code == 302
        workspace_for_test_user.refresh_from_db()
        assert workspace_for_test_user.name == 'Updated Workspace'
        assert workspace_for_test_user.description == 'Updated description'


class TestSettingsHomeView:
    view_name = 'customer_accounts.settings_home'

    @pytest.mark.django_db
    def test_settings_home_view_requires_login(self, client):
        helpers.assert_view_requires_login(client, view_name=self.view_name)

    @pytest.mark.django_db
    def test_settings_home_view_renders_template(self, client, basic_test_user_and_account):
        test_user, _ = basic_test_user_and_account
        helpers.assert_view_renders_template(
            client, view_name=self.view_name,
            template_name='customer_accounts/settings_home.html',
            user=test_user
        )
