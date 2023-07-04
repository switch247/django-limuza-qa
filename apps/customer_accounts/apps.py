from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customer_accounts'


ROLES = [
    {
        'nice_name': 'Account Owner',
        'name': 'account_owner'
    },
    {
        'nice_name': 'Manager',
        'name': 'manager'

    },
    {
        'nice_name': 'Admin',
        'name': 'admin'
    },
    {
        'nice_name': 'Agent',
        'name': 'agent'
    },
    {
        'nice_name': 'Lead',
        'name': 'lead',
    },
    {
        'nice_name': 'Superuser',
        'name': 'superuser'
    },
]

SUBSCRIPTION_PLANS = [
    {
        'name': 'Basic',
        'price': 1000
    },
    {
        'name': 'Pro',
        'price': 2000
    },
    {
        'name': 'Enterprise',
        'price': 5000
    }
]
