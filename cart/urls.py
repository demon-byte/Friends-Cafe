from django.urls import path
from .views import view_cart, add_to_cart, update_cart_item, remove_from_cart

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]