from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# todo buld profile view to change account there
# todo - not sure if every user should have right to do this?
# @login_required
# def add_user_to_account(request):
#     if request.method == 'POST':
#         form = forms.AddUserForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             account = request.user.account
#             create_user_for_account(account, username, password)
#             return redirect('customer_accounts.workspaces_list')
#     else:
#         form = forms.AddUserForm()
#     return render(request, 'customer_accounts/add_user_to_account.html', {'form': form})


@login_required
def edit_user_info(request):
    # TODO: Implement the edit user information view
    # check if this can be done from allauth (for first name, last name and email)
    return render(request, 'customer_accounts/edit_user_info.html', {})


@login_required
def enable_2fa(request):
    # TODO: Implement the enable 2-factor authentication view
    return render(request, 'customer_accounts/enable_2fa.html', {})


@login_required
def set_session_timeout(request):
    # TODO: Implement the set session timeout view
    # this is done in settings.py
    return render(request, 'customer_accounts/set_session_timeout.html', {})


@login_required
def sso_settings(request):
    # TODO: Implement the SSO/AD login settings view
    return render(request, 'customer_accounts/sso_settings.html', {})


@login_required
def add_user_to_workspace(request, workspace_id):
    # TODO: Implement the add user to workspace view, implement django invitations
    return render(request, 'customer_accounts/add_user_to_workspace.html', {})


def switch_workspace(request, workspace_id):
    # TODO: Implement the switch workspace functionality.
    return render(request, 'customer_accounts/add_user_to_workspace.html', {})


def bulk_add_user(request):
    # TODO: Implement the switch workspace functionality.
    # this could be done via bulk invite if needed
    return render(request, 'customer_accounts/add_user_to_workspace.html', {})


def list_users(request):
    # Todo, should be have some sort of filter
    # implement some version of https://datatables.net/
    return render(request, 'account/add_user_to_workspace.html', {})
