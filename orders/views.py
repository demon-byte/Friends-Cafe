from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    
    if cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('menu_list')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_price=cart.total_price,
                delivery_address=form.cleaned_data['delivery_address'],
                delivery_notes=form.cleaned_data['delivery_notes'],
                payment_method=form.cleaned_data['payment_method'],
            )
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price,
                )
            
            # Deactivate cart
            cart.is_active = False
            cart.save()
            
            messages.success(request, f"Order #{order.order_number} placed successfully!")
            return redirect('order_detail', order_id=order.id)
    else:
        initial_data = {}
        if request.user.profile.default_address:
            initial_data['delivery_address'] = request.user.profile.default_address
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})