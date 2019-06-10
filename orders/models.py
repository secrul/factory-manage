from django.db import models
from warehouse.models import Product

class Orders(models.Model):#订单
    order_name=models.ForeignKey(Product,on_delete=models.DO_NOTHING, verbose_name="产品名称")
    order_client=models.CharField(max_length=100, verbose_name="客户名称")
    order_number = models.IntegerField(verbose_name="数量")
    order_price=models.IntegerField(verbose_name="单价(元)")
    order_total_price = models.IntegerField(verbose_name="总价(元)")
    order_time = models.DateField(auto_now_add=True, verbose_name="订货时间")
    order_end = models.DateField(verbose_name="交货时间")
    order_supplement=models.TextField(verbose_name="补充",null=True, blank=True)

    class Meta:
        ordering = ['-order_time']
