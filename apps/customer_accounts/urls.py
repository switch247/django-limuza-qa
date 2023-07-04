from django.urls import path
from apps.customer_accounts import views

urlpatterns = [
    path('workspaces/', views.view_workspaces, name='customer_accounts.workspaces_list'),
    path('workspaces/create/', views.create_workspace, name='customer_accounts.create_workspace'),
    path('workspaces/edit/<int:workspace_id>/', views.edit_workspace, name='customer_accounts.edit_workspace'),
    # path('account/add_user/', views.add_user_to_account, name='add_user_to_account'),
    path('settings/', views.settings_home, name='customer_accounts.settings_home')
]
