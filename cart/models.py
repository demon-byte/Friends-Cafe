from django.db import models
from django.conf import settings
from menu.models import MenuItem

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def active_cart_items_count(self):
        if self.is_active:
            return self.items.count()
        return 0
    def __str__(self):
        return f"Cart #{self.id} - {self.user.email}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'item')

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    @property
    def total_price(self):
        return self.item.price * self.quantity