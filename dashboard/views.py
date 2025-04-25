from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from orders.models import Order
from menu.models import MenuItem, Category
from django_tables2 import RequestConfig
from .tables import OrderTable, MenuItemTable
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from .forms import MenuItemForm, CategoryForm

def staff_required(user):
    return user.is_staff

# Dashboard Home View
@login_required
@user_passes_test(staff_required)
def dashboard_home(request):
    stats = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'revenue': Order.objects.filter(payment_status='paid').aggregate(
            total=Sum('total_price')
        )['total'] or 0
    }

    recent_orders = OrderTable(
        Order.objects.all().order_by('-created_at'),
        prefix='recent-'
    )

    RequestConfig(
        request, 
        paginate={'per_page': 5}
    ).configure(recent_orders)

    context = {
        **stats,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/home.html', context)

# Order Views
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'dashboard/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = OrderTable(self.get_queryset())
        return context

@login_required
@user_passes_test(staff_required)
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.ORDER_STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.order_number} status updated to {order.get_status_display()}.")
        else:
            messages.error(request, "Invalid status.")
    
    return redirect('dashboard:order_list')

# Menu Item Views
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'dashboard/menu_item_list.html'
    context_object_name = 'items'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_filter = self.request.GET.get('category')
        if category_filter:
            queryset = queryset.filter(category__slug=category_filter)
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = MenuItemTable(self.get_queryset())
        context['categories'] = Category.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemCreateView(SuccessMessageMixin, CreateView):
    model = MenuItem  # This was missing in your original code
    form_class = MenuItemForm
    template_name = 'dashboard/menu_item_form.html'
    success_message = "Menu item created successfully!"
    
    def get_success_url(self):
        return reverse('dashboard:menu_item_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemUpdateView(SuccessMessageMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'dashboard/menu_item_form.html'
    success_message = "Menu item updated successfully!"
    
    def get_success_url(self):
        return reverse('dashboard:menu_item_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemDeleteView(SuccessMessageMixin, DeleteView):
    model = MenuItem
    template_name = 'dashboard/menu_item_confirm_delete.html'
    success_message = "Menu item deleted successfully!"
    
    def get_success_url(self):
        return reverse('dashboard:menu_item_list')

# Category Views
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return super().get_queryset().order_by('name')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_message = "Category created successfully!"
    
    def get_success_url(self):
        return reverse('dashboard:category_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_message = "Category updated successfully!"
    
    def get_success_url(self):
        return reverse('dashboard:category_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required), name='dispatch')
class CategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = Category
    template_name = 'dashboard/category_confirm_delete.html'
    success_message = "Category deleted successfully!"
    
    def get_success_url(self):
        return reverse('dashboard:category_list')