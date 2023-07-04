from django.urls import path
from .views import show_agent_dashboard, show_dashboard, ticket_assignment_dashboard, assignment_rule_list, create_assignment_rule, create_ticket_assignment, ticket_assignment_list,create_ticket_review,change_scorecard, show_review, save_review, create_category, create_scorecard, list_categories, list_scorecards, list_reviews, view_category, view_scorecard, create_ticket_assignment_add_filter

urlpatterns = [
    path('create-ticket-review/<str:ticket_id>/', create_ticket_review, name='create_ticket_review'),
    path('review/<str:review_id>/', show_review, name='show_review'),
    path('review/<str:review_id>/edit', change_scorecard, name='edit_review'),
    path('review/<str:review_id>/save', save_review, name='save_review'),
    path('categories/', list_categories, name='list_categories'),
    path('scorecards/', list_scorecards, name='list_scorecards'),
    path('categories/new', create_category, name='create_category'),
    path('scorecards/new', create_scorecard, name='create_scorecard'),
    path('reviews/new/<str:ticket_id>/', create_ticket_review, name='create_review'),
    path('', list_reviews, name='list_reviews'), 
    path('categories/<str:category_id>/', view_category, name='view_category'),  # Add this line
    path('scorecards/<str:scorecard_id>/', view_scorecard, name='view_scorecard'),  # Add this line
    path('assignment_dashboard/', ticket_assignment_list, name='ticket_assignment_dashboard'),
    path('assignment-rules/', assignment_rule_list, name='assignment_rule_list'),
    path('assignment-rules/new/', create_assignment_rule, name='create_assignment_rule'),
    path('ticket-assignments/', ticket_assignment_list, name='ticket_assignment_list'),
    path('ticket-assignments/new/', create_ticket_assignment, name='create_ticket_assignment'),
    path('ticket-assignments/new/add_filter', create_ticket_assignment_add_filter, name='create_ticket_assignment_add_filter'),
    path('dashboard/', show_dashboard, name='show_dashboard'),
    path('agent/dashboard/', show_agent_dashboard, name='show_agent_dashboard'),
]
