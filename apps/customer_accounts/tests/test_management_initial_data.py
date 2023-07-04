from django.core.management import call_command

import pytest

from apps.customer_accounts import models


@pytest.mark.django_db
def test_management_initial_data():
    call_command('initial_setup')

    roles = models.Role.objects.all()
    assert roles.count() == 6

    plans = models.SubscriptionPlan.objects.all()
    assert plans.count() == 3
