# Migrations Cheat Sheet

## 1. Migration rollback

To reverse last migration use
```
python3 manage.py migrate app_name number
```

for example to roll back migration 0001 in accounts:
```
python3 manage.py migrate accounts zero
```

to roll back migration 0002 in accounts:
```
python3 manage.py migrate accounts 0001
```

Rollback is only possible if we still have the file that we want to roll back (it was not deleted or modified). In some cases rollback is not possible due to specific changes that this migration applied or if it broke during running.

Rollback may roll more than one app in the same time, if these migrations are related. 

## 2. Wipe migrations and reset_db:
**Warning:** this delets all data - see below to load initial data, when project goes live this will no longer be an option.

```bash
find ./your_project_directory -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./path_to_exclude/*" -delete
find ./your_project_directory -path "*/migrations/*.pyc" -not -path "./path_to_exclude/*" -delete

python manage.py reset_db
python manage.py makemigrations
```

Deleting migrations alone does not solve the problem, because database holds the state of previously applied migrations. That is why you need to reset_db or roll back migration.

## 3. Data load

After wiping out database or rolling back to zero you may need to upload initial data for accounts app. Otherwise you will not be able to create any user
```
python3 manage.py inital_setup
```

You can also use fixtures to load. Currently docker loads them automatically on docker up.
