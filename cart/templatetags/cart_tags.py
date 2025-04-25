from django import template
from cart.models import Cart

register = template.Library()

@register.filter(name='get_user_cart_count')
def get_user_cart_count(user):
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user, is_active=True).first()
        return cart.items.count() if cart else 0
    return 0