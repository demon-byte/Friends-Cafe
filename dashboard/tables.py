import django_tables2 as tables
from orders.models import Order
from menu.models import MenuItem

class OrderTable(tables.Table):
    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap5.html"
        fields = ("order_number", "user", "status", "payment_status", "total_price", "created_at")
        order_by = "-created_at"  # Default sorting

class MenuItemTable(tables.Table):
    class Meta:
        model = MenuItem
        template_name = "django_tables2/bootstrap5.html"
        fields = ("name", "category", "price", "is_available")

class OrderTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='dashboard/order_actions.html',
        orderable=False
    )

    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap5.html"
        fields = ("order_number", "user", "status", "payment_status", "total_price", "created_at", "actions")