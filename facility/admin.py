from django.contrib import admin
from .models import Facility, Maintain, Repair

# Register your models here.
@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("id", "facility_name", "version","price", "buyer", "buy_time")


@admin.register(Maintain)
class MaintainAdmin(admin.ModelAdmin):
    list_display = ("facility_id", "last_time", "staff_name", "complmentary")


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ("facility_id" , "baoxiu_staff_name","baoxiu_staff_tel", "baoxiu_time", "baoxiu_complementary", "repair_staff_name", "repair_time")

