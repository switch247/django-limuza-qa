"""
URL configuration for limuza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.generic.base import TemplateView

import debug_toolbar

from limuza import views
# ADDED BY SMARTDEV CODE

admin.autodiscover()


urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    # ADDED BY SMARTDEV-CODE 08/16/2024
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('workspace/', include('apps.customer_accounts.urls')),
    path('tickets/', include('apps.tickets.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path("accounts/", include("allauth.urls")),
    path("invitations/", include('invitations.urls', namespace='invitations')),
    # path("accounts/profile/", TemplateView.as_view(template_name="profile.html"), name='profile'),
    path("i18n/", include("django.conf.urls.i18n")),

    # New paths
    path("reviews/", TemplateView.as_view(template_name="index.html"), name='reviews'),
    path("coaching/", TemplateView.as_view(template_name="index.html"), name='coaching'),
    path("assignments/", TemplateView.as_view(template_name="index.html"), name='assignments'),
    path("conversations/", TemplateView.as_view(template_name="index.html"), name='conversations'),
    # for dev reloading
    path("__reload__/", include("django_browser_reload.urls"))
]
