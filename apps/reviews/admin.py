from django.contrib import admin

from apps.reviews import models

admin.site.register(models.Category)
admin.site.register(models.Scorecard)
admin.site.register(models.ScorecardCategory)
admin.site.register(models.Review)
admin.site.register(models.TicketReview)
admin.site.register(models.ConversationReview)
admin.site.register(models.ReviewCategory)
admin.site.register(models.AssignmentRule)
admin.site.register(models.TicketAssignment)
admin.site.register(models.AssignmentDashboard)
