from django.contrib import admin
from .models import Warehouse, PurchaseList, ProduceDiary, Product, Goods, WarehouseSource

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "current_time", "product_name", "number", "unit")


@admin.register(WarehouseSource)
class WarehouseSourceAdmin(admin.ModelAdmin):
    list_display = ("id", "current_time", "source_name", "number", "unit")


@admin.register(PurchaseList)
class PurchaseListAdmin(admin.ModelAdmin):
    list_display = ("good_name", "good_version", "good_num", "apply_staff_name", "apply_date",
                    "sanction_staff_name", "sanction_date", "price", "total_price",
                    "buyer_name", "buyer_date", "price", "total_price")


@admin.register(ProduceDiary)
class ProduceDiaryAdmin(admin.ModelAdmin):
    list_display = ("id", "current_time", "staff_name",  "product_name", "today_done_num", "qualified_num")


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ("id", "good_name")
