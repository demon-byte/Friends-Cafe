from django.contrib import admin
from orders.models import Order, OrderItem 

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total_price', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__email', 'user__username']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'user', 'total_price', 'created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_price', 'created_at')
        }),
        ('Delivery Information', {
            'fields': ('delivery_address', 'delivery_notes')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_method')
        }),
    )