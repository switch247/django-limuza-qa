from django.contrib.auth import get_user_model
from apps.customer_accounts.models import Workspace, CustomerAccount
from apps.customer_accounts.services import create_user_and_account, create_user_for_account, create_workspace_and_workspace_user_for_account

User = get_user_model()


def create_admin_user_and_account(admin):
    username = 'testuser'
    password = 'testpass'
    user, account = create_user_and_account(username, password)
    # get workspace
    workspace = Workspace.objects.first()
    user.is_superuser = True
    user.save()
    return user, account, workspace


def create_test_account(user, account_name="Test Account", admin=False):
    """
    Create an Account and assign the given user as the AccountOwner.

    Args:
        user (User): The user who will own the new account.
        account_name (str): Name for the account.

    Returns:
        Account: The created account.
    """
    account = CustomerAccount.objects.create(name=account_name, owner=user)
    default_workspace_name = f"{account_name} Workspace"
    workspace = Workspace.objects.create(name=default_workspace_name, account=account)
    # workspace_user = WorkspaceUser.objects.create(user=user, workspace=workspace)
    # workspace_user.is_admin = admin
    # workspace_user.save()
    # if admin:
    #     WorkspaceOwner.objects.create(workspace=workspace, workspace_user=workspace_user)
    user.profile.account = account
    user.save()
    return account


def create_test_user(username='testuser', password='testpass', role='Account Owner'):
    """
    Create a test user.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        role (str): The role for the new user.

    Returns:
        User: The created user.
    """
    user = User.objects.create_user(username=username, password=password)
    user.role = role
    user.save()
    return user
