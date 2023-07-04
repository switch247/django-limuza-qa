from django.shortcuts import render, redirect, get_object_or_404
from apps.reviews.models import TicketReview, ReviewCategory, Category
from django.contrib.auth.decorators import login_required
from apps.reviews.models import TicketReview, Scorecard
from apps.tickets.models import Ticket
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from ..forms import *
from ..models import *

User = get_user_model()

@login_required
def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories/list_categories.html', {'categories': categories})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('list_categories')
    else:
        form = CategoryForm()

    context = {
        'form': form
    }
    return render(request, 'categories/create_category.html', context)

@login_required
def view_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'view_category.html', {'category': category})