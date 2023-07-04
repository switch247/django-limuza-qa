from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_multitenant.utils import set_current_tenant

from apps.customer_accounts import models
from apps.customer_accounts import forms


@login_required
def settings_home(request):
    current_tenant = request.user.profile.account
    set_current_tenant(current_tenant)
    return render(request, 'customer_accounts/settings_home.html')


@login_required
def view_workspaces(request):
    account = request.user.profile.account
    set_current_tenant(account)
    workspaces = models.Workspace.objects.filter(account=account)
    return render(request, 'customer_accounts/view_workspaces.html', {'workspaces': workspaces})


@login_required
def create_workspace(request):
    if request.method == 'POST':
        form = forms.WorkspaceForm(request.POST)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.account = request.user.profile.account
            workspace.save()
            return redirect('customer_accounts.workspaces_list')
    else:
        form = forms.WorkspaceForm()
    return render(request, 'customer_accounts/create_workspace.html', {'form': form})


@login_required
def edit_workspace(request, workspace_id):
    workspace = get_object_or_404(models.Workspace, id=workspace_id, account=request.user.profile.account)
    if request.method == 'POST':
        form = forms.WorkspaceForm(request.POST, instance=workspace)
        if form.is_valid():
            form.save()
            return redirect('customer_accounts.workspaces_list')
    else:
        form = forms.WorkspaceForm(instance=workspace)
    return render(request, 'customer_accounts/edit_workspaces.html', {'form': form, 'workspace': workspace})
