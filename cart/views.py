from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from menu.models import MenuItem
from .models import Cart, CartItem

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    return render(request, 'cart/view_cart.html', {'cart': cart})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{item.name} added to your cart.")
    return redirect('menu_list')

@login_required
def update_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
    except ValueError:
        messages.error(request, "Invalid quantity.")
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

