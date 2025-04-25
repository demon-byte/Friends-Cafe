from django.shortcuts import render
from menu.models import Category, MenuItem

def home_view(request):
    categories = Category.objects.filter(is_active=True)
    featured_items = MenuItem.objects.filter(is_available=True).order_by('?')[:8]
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_items': featured_items
    })