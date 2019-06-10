from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from facility.models import Facility
from django.contrib.auth.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name


class Goods(models.Model):
    good_name = models.CharField(max_length=100)

    def __str__(self):
        return self.good_name


class Warehouse(models.Model):#仓库
    current_time = models.DateField(auto_now_add=True, verbose_name="日期")
    product_name = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name="产品类型", null=True)
    number = models.IntegerField(verbose_name="数量", null=True)
    unit = models.CharField(verbose_name="单位", null=True, max_length=10)

    class Meta:
        ordering = ['-current_time']


class WarehouseSource(models.Model):#仓库
    current_time = models.DateField(auto_now_add=True, verbose_name="日期")
    source_name = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name="原料类型", null=True)
    number = models.IntegerField(verbose_name="数量", null=True)
    unit = models.CharField(verbose_name="单位", null=True, max_length=10)

    class Meta:
        ordering = ['-current_time']


class PurchaseList(models.Model):#采购单
    good_name = models.CharField(max_length=100, verbose_name="品名")
    good_version = models.CharField(max_length=100, verbose_name="型号")
    good_num = models.IntegerField(verbose_name="数量")
    apply_staff_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="申请人",null=True,blank=True, related_name='purchase_a')
    apply_date = models.DateField(auto_now_add=True, verbose_name="申请日期")
    sanction_staff_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="批准人", null=True,blank=True,related_name='purchase_b')
    sanction_date = models.DateField(auto_now=True, verbose_name="批准日期",null=True,blank=True)
    price = models.BigIntegerField(null=True,blank=True,verbose_name="单价")
    total_price = models.BigIntegerField(verbose_name="总价",null=True,blank=True)
    buyer_name = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True, verbose_name="采购员", related_name='purchase_c')
    buyer_date = models.DateField(auto_now=True, verbose_name="采购日期",null=True,blank=True)

    class Meta:
        ordering = ['-apply_date']


class ProduceDiary(models.Model):#生产日记
    current_time = models.DateField(auto_now_add=True, verbose_name="日期")
    facility_id = models.ForeignKey(Facility, verbose_name="设备", on_delete=models.DO_NOTHING)
    staff_name = models.ForeignKey(User, verbose_name="员工", on_delete=models.DO_NOTHING)
    product_name = models.ForeignKey(Product, verbose_name="产品", on_delete=models.DO_NOTHING)
    today_done_num = models.IntegerField(default=0, verbose_name="今日产量")
    qualified_num = models.IntegerField(default=0, verbose_name="合格量")

    class Meta:
        ordering = ['-current_time']
