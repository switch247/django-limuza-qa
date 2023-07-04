from django.db import transaction
from django.contrib.auth import get_user_model

from django_multitenant.utils import set_current_tenant, unset_current_tenant

from apps.customer_accounts.models import CustomerAccount, Workspace

User = get_user_model()

@transaction.atomic
def create_user_and_account(username, password, account_name=None):
    """
    Create a User, an Account, and a default Workspace. 
    Assign the user as the owner of the account and as a WorkspaceUser of the default Workspace.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        account_name (str): Optional name for the account. Defaults to "{username}'s Account".

    Returns:
        User: The created user.
        Account: The created account.
    """
    # Create the user
    user = User.objects.create_user(username=username, password=password)
    
    # Create the account
    if account_name is None:
        account_name = f"{username}'s Account"
    
    account = CustomerAccount.objects.create(name=account_name, owner=user)
    set_current_tenant(account)
    # Create the default workspace
    default_workspace_name = f"{username}'s Default Workspace"
    workspace = create_workspace_and_workspace_user_for_account(account, default_workspace_name, user)

   
    
    # Link the user to the account
    user.profile.account = account
    user.save()
    unset_current_tenant()
    return user, account

@transaction.atomic
def create_user_for_account(account, username, password, is_owner=False, user_role='User'):
    """
    Create a User and assign them to the given account.

    Args:
        account (Account): The account to which the user will be assigned.
        username (str): The username for the new user.
        password (str): The password for the new user.
        is_owner (bool): Whether the user should be the Account owner. Defaults to False.
        user_role (str): The role of the user. Defaults to 'User'.

    Returns:
        User: The created user.
    """
    user = User.objects.create_user(username=username, password=password)
    
    if is_owner:
        # todo add role not owner value
        account.save()
    
    user.profile.account = account
    user.save()
    return user


@transaction.atomic
def create_workspace_and_workspace_user_for_account(account, workspace_name, user):
    """
    Create a Workspace for the given account and assign a user to it.

    Args:
        account (Account): The account to which the workspace will belong.
        workspace_name (str): The name of the new workspace.
        user (User): The user who will be assigned to the workspace.

    Returns:
        Workspace: The created workspace.
    """
    workspace = Workspace.objects.create(name=workspace_name, account=account)
    # WorkspaceUser.objects.create(user=user, workspace=workspace)
    return workspace
