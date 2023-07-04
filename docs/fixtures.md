# Fixtures

## Django docs

Django docs on creating fixtures [here](https://django-testing-docs.readthedocs.io/en/latest/fixtures.html#how-to-create-a-fixture)

Django docs on natural key [here](https://django-testing-docs.readthedocs.io/en/latest/fixtures.html#how-to-create-a-fixture)

## Docker

Currently docker tries to load fixtures on `docker compose up`


## Basic commands:

### Creating data dump:

go inside web container:
```
docker exec -it limuza-web-1 bash
```

dump data into a fixture in accounts, where json will have indenation 2 (this can be increased):

```
python3 manage.py dumpdata accounts --indent=2 > apps/accounts/fixtures/accounts.json
```

tickets app:
```
python3 manage.py dumpdata accounts --indent=2 > apps/tickets/fixtures/tickets.json
```

reviews app:
```
python3 manage.py dumpdata accounts --indent=2 > apps/reviews/fixtures/reviews.json
```

integrations app:
```
python3 manage.py dumpdata accounts --indent=2 > apps/integrations/fixtures/integrations.json
```


### Creating data dump with natural keys:

Creating data dump with natural keys is only possible if models are ready for it (example: Roles model in accounts app):

- ideally model needs to have one unique field that will become natural identifier, it has to be set unique=True, null=False, blank=False. I use slug field AutoSlugField for this.
- model needs a method natural_key returning tuple of the unique field
- if we don't have one unique field, we may use unique_together and use combination of two or more fields for natural key
- next step: add model manager class that has a method get_by_natural_key
- next step: to the model add new field objects = YourManagerClass

To dump data you need to use natural primary and natural foreign. Data dump created this way should not contain "pk" (id). This is one long command:

```
python3 manage.py dumpdata accounts --indent=2 --natural-primary --natural-foreign > apps/accounts/fixtures/accounts.json
```


### Shell plus

Creating instances can also be done in shell_plus

go inside web container:
```
docker exec -it limuza-web-1 bash
```
go to shell_plus:
```
python3 manage.py shell_plus
```

We can run normal django ORM commands to create objects:

```
FreshdeskIntegration.objects.create(
        name=integration_data['name'],
        account=account,
        type=integration_type,
        integration_key=integration_data['integration_key'],
        workspace=workspace,
        created_by=admin_user,
        active=integration_data.get('active', True),
        details=integration_data.get('details', {})
    )
```
