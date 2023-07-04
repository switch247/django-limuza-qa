from django.contrib import admin

from apps.tickets import models

admin.site.register(models.Ticket)
admin.site.register(models.Conversation)
