from django.urls import path
from . import views
from .views import (
    dashboard_home, OrderListView, MenuItemListView, MenuItemCreateView,
    MenuItemUpdateView, MenuItemDeleteView, CategoryListView, CategoryCreateView,
    CategoryUpdateView, CategoryDeleteView, update_order_status
)
app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_home, name='home'),

    # Orders
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/update-status/', update_order_status, name='update_order_status'),
    
    # Menu Items
    path('menu-items/', MenuItemListView.as_view(), name='menu_item_list'),
    path('menu-items/add/', MenuItemCreateView.as_view(), name='menu_item_add'),
    path('menu-items/<int:pk>/edit/', MenuItemUpdateView.as_view(), name='menu_item_edit'),
    path('menu-items/<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu_item_delete'),
    
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]