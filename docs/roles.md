# Roles and permissions
to view table correctly use preview 

## Roles
List of roles can be found: apps/accounts/apps.py ROLES

This is the list that gets loaded if you run command `python3 manage.py inital_setup`

list can be modified

## Permissions:
R read
E edit
El edit limited to some fields
C create
D delete

Superuser: everything

## Permisions & roles & models:


| Model    | Account Owner | Manager | Admin | Agent | Lead | Superuser
| -------- | ------- | -------- | ------- | -------- | ------- |------- |
| CustomerAccount  | everything  | ?  | ?    | ? |  ?   | everything    |
| CustomInvitations | ?     | ?  | ?   | ?  | ?    | everything    |
| Profile    | ?    | ?  | ?   | ?  | ?   | everything    |