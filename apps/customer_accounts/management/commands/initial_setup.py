from django.core.management.base import BaseCommand, CommandError
from apps.customer_accounts import models

from apps.customer_accounts import apps


class Command(BaseCommand):
    help = 'If database is empty, this command will setup the initial data'

    def create_roles(self):
        try:
            roles = apps.ROLES

            for role in roles:
                models.Role.objects.create(**role)
            roles = models.Role.objects.all()
            self.stdout.write(self.style.SUCCESS(f'Successfully created {roles.count()} roles'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating roles: {e}'))

    def create_subscription_plans(self):
        try:
            plans = apps.SUBSCRIPTION_PLANS
            for plan in plans:
                models.SubscriptionPlan.objects.create(**plan)
            plans = models.SubscriptionPlan.objects.all()
            self.stdout.write(self.style.SUCCESS(f'Successfully created {plans.count()} subscription plans'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating subscription plans: {e}'))

    def handle(self, *args, **options):
        if models.Role.objects.all():
            self.stdout.write(self.style.SUCCESS('Roles already exist'))
        self.create_roles()
        self.create_subscription_plans()
        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))
