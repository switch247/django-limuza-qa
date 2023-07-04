# Documentation for accounts app

## Initial setup:

After starting database from reset - run inside web container
```
docker exec -it limuza-web-1 bash

python3 manage.py initial_setup
```
This creates Roles and SubscriptionPlans, needed before first user can be created.

The initial data is stored in apps/accounts/apps.py `ROLES` and `SUBSCRIPTION_PLANS`. These constances are called by management command as well as by the tests to create fixtures.

## Database schema

Database schema can be found [here](https://dbdiagram.io/d/limuza-66adf57f8b4bb5230e1e38ee)


## Tenant

Customer accounts is main TenantModel, Most other models have field that adds relation to this TenantModel.  There are some models Tenant agnostic - like Roles.

Each model that is related to CustomerAccounts needs to have `account` field with ForeignKey to CustomerAccounts and `tenant_id = account_id`. It also needs to inherit from TenantModel from django multitenantcy

Model that is tenant agnostic needs to inherit from django models.Model.

## Profile

Relation between user and CustomerAccount is through Profile (one to one). User can only belong to one CustomerAccount.

User can belong to many Workspaces

User gets assigned Role in profile.


## Customer Account

This is main Tenant Model. It is related to Subscription. Each Tenant Model can have one or many subscriptions. Subscriptions are related to SubscriptionPlan that suggests prices and names for Subscription Plans.

## Workspace

CustomerAccount model can have many workspaces. User can belong to many workspaces.

## Custom Invitation
Invitation model from django-invitation that has been customised to include CustomerAccount, Workspace and Role for the invited user.

Invitations that are not acted on will get deleted in 7 days. This can be changed in settings.

Invitations that are accepted stay in the database.

## Tests

to run tests
```
docker exec -it limuza-web-1 bash

pytest
```
Tests for models are only covering the parts that were customised. Any custom save method should be tested. I also test signal.

Tests for views:
- test if view is protected against unauthenticated user
- test if view is protected against user from a different CustomerAccount
- test if view renders template
- test post method for view

