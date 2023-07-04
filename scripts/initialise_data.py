import os
from django.core.management import call_command
from django.db.utils import OperationalError
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

from apps.customer_accounts import models
from apps.customer_accounts import apps

User = get_user_model()

def run():
    try:
        print("Setting up initial data...")

        # Load initial roles and subscription plans
        # roles_list = apps.ROLES
        # for role in roles_list:
        #     models.Role.objects.get_or_create(**role)

        # subscription_plans_list = apps.SUBSCRIPTION_PLANS
        # for plan in subscription_plans_list:
        #     models.SubscriptionPlan.objects.get_or_create(**plan)

        # Create the user
        email = os.getenv('USER_EMAIL', 'james.bond@example.com')
        password = os.getenv('USER_PASSWORD', 'topsecret')
        
        user = get_user_model().objects.create_user(
            email=email,
            username= 'jamesb',
            first_name= 'James',
            last_name= 'Bond',
            password= password
        )
        # Ensure the user's email is verified
        EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            defaults={'primary': True, 'verified': True}
        )

        # Create the account and workspace for the user
        account, _ = models.CustomerAccount.objects.get_or_create(name='MI6')
        workspace = models.Workspace.objects.get_or_create(
            name='Test Workspace',
            account=account,
            description='Workspace for testing'
        )

        # Associate the user with the account and workspace (assuming a profile or similar relation exists)
        profile = user.profile  # Adjust if your user model has a different relation
        profile.save()

        # Make the user an admin
        user.is_superuser = True
        user.is_staff = True
        user.save()

        print(f"Superuser {email} set up with the new password.")

    except OperationalError as e:
        print(f"Database error occurred: {e}")
        print("Make sure the database is ready and try again.")
    except User.DoesNotExist:
        print(f"No user found with the email {email}.")
