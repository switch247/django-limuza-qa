from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
