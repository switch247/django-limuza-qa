# this got very complicated very quickly lol. This is the brief explanation:
# categories make up scorecards, but they don't have to be and not with the same weighting
# To different departments, tone can mean more than another as an example but we don't want 2 tone categories - ScorecardCategory solves this
# They can be used in multiple.
# 
# Reviews can be done on two levels, tickets and conversations so we should be able to do this now already.
# ReviewCategory solves the fact that categories are the "bases" and the actual values should be related to a review
# Category: Defines scales and N/A option.
# Scorecard: Represents a scorecard with related categories.
# ScorecardCategory: Links scorecards to categories with additional fields like weighting.
# Review: Base class for reviews, with methods to check review type.
# TicketReview: Inherits from Review and links to Ticket.
# ConversationReview: Inherits from Review and links to Conversation.
# ReviewCategory: Stores category evaluations within a review.
from django.contrib.auth import get_user_model

from django.conf import settings
from django.db import models
from django_multitenant.models import TenantModel

from apps.tickets.models import Ticket, Conversation
from apps.customer_accounts.models import Workspace, TenantClass, TenantForeignKey 

User = get_user_model()


class Category(TenantModel):
    SCALE_CHOICES = [
        ('binary', 'Binary'),
        ('3_point', '3 Point'),
        ('5_point', '5 Point'),
        ('7_point', '7 Point'),
    ]

    name = models.CharField(max_length=255)
    scale = models.CharField(max_length=50, choices=SCALE_CHOICES)
    allow_na = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'scale': self.scale,
            'allow_na': self.allow_na,
        }

class Scorecard(TenantClass):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scorecards')
    workspace = TenantForeignKey(Workspace, on_delete=models.CASCADE, related_name='workspace')

    def __str__(self):
        return self.name
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
    def get_categories(self):
        return ScorecardCategory.objects.filter(scorecard=self).select_related('category')

class ScorecardCategory(TenantClass):
    scorecard = TenantForeignKey(Scorecard, on_delete=models.CASCADE, related_name='scorecard_categories')
    category = TenantForeignKey(Category, on_delete=models.CASCADE, related_name='scorecard_categories')
    weighting = models.FloatField(default=1.0)

    class Meta:
        unique_together = ('scorecard', 'category')

    def __str__(self):
        return f"{self.scorecard.name} - {self.category.name}"
    
    def to_json(self):
        return {
            'id': self.id,
            'scorecard': self.scorecard.to_json(),
            'category': self.category.to_json(),
            'weighting': self.weighting
        }

class Review(TenantClass):
    scorecard = TenantForeignKey(Scorecard, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    date = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(default=True)  # Added field for draft status
    comments = models.TextField()

    def is_ticket_review(self):
        return hasattr(self, 'ticketreview')

    def is_conversation_review(self):
        return hasattr(self, 'conversationreview')
    
    def get_review_data(self):
        """
        Retrieves the necessary data for the review form.
        If there are review categories, return those.
        Otherwise, return the scorecard categories for the scorecard linked to the review.
        """
        review_categories = self.review_categories.all().select_related('scorecard_category__category')
        if review_categories.exists():
            review_data = [rc.to_json() for rc in review_categories]
            scorecard_categories = None
        else:
            scorecard_categories = self.scorecard.get_categories()
            review_data = [sc.to_json() for sc in scorecard_categories]
            review_categories = None
        return review_data, scorecard_categories, review_categories
    
    def get_categories(self):
        rc = ReviewCategory.objects.filter(review=self).select_related('scorecard_category__category')
        if rc.exists():
            return rc
        else:
            return self.scorecard.get_categories()

    def update_scorecard(self, scorecard):
        # update/save the scorecard, returns all scorecard_categories
        self.scorecard = scorecard
        self.save()
        return self.get_categories()

    def __str__(self):
        return f"Review {self.id}"

class TicketReview(Review):
    ticket = TenantForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_reviews')

class ConversationReview(Review):
    conversation = TenantForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation_reviews')

class ReviewCategory(TenantClass):
    review = TenantForeignKey(Review, on_delete=models.CASCADE, related_name='review_categories')
    scorecard_category = TenantForeignKey(ScorecardCategory, on_delete=models.CASCADE, related_name='review_categories')
    score = models.IntegerField(null=True, blank=True)  # Assuming the score is an integer
    na = models.BooleanField(default=False)

    class Meta:
        unique_together = ('review', 'scorecard_category')

    def __str__(self):
        return f"{self.review.id} - {self.scorecard_category.category.name}"

    def to_json(self):
        sc = self.scorecard_category
        return {
            'id': self.id,
            'score': self.score,
            'na': self.na,
            'scorecard_category': sc.to_json()
        }

class AssignmentRule(TenantClass):
    # TODO create methods that will create ticket assignments on a regular basis automatically.
    name = models.CharField(max_length=255)
    reviewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assignment_rules')
    description = models.TextField()
    criteria = models.JSONField() 

    def __str__(self):
        return self.name

class TicketAssignment(TenantClass):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    assignment_rule = TenantForeignKey(AssignmentRule, on_delete=models.CASCADE, related_name='ticket_assignments')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ticket_assignments')
    reviews = models.ManyToManyField('reviews.Review', related_name='ticket_assignments')
    completion_percentage = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.assignment_rule.name} - {self.reviewer.username} - {self.status}"

class AssignmentDashboard(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_dashboards')

    def get_ticket_assignments(self):
        return TicketAssignment.objects.all()

    def get_user_workload(self, user):
        return TicketAssignment.objects.filter(agent=user).count() + TicketAssignment.objects.filter(reviewer=user).count()

    def adjust_assignment_rules(self, rule_id, new_criteria):
        rule = AssignmentRule.objects.get(id=rule_id)
        rule.criteria = new_criteria
        rule.save()
        return rule

    def __str__(self):
        return f"Dashboard for manager {self.manager.username}"

        return f"Dashboard for manager {self.manager.username}"