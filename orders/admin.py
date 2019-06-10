from django.contrib import admin
from .models import Orders

# Register your models here.
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "order_name", "order_client",  "order_price", "order_number", "order_total_price", "order_time", "order_end", "order_supplement")