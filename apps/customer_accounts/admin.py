# apps/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.customer_accounts import models



admin.site.register(models.Workspace)
admin.site.register(models.CustomerAccount)
admin.site.register(models.Role)
