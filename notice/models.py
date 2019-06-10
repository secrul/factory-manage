from django.db import models
from django.contrib.auth.models import User


class Notice(models.Model):
    title = models.CharField(max_length=100,verbose_name="标题")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="发表人", null=True)
    created_time = models.DateField(auto_now_add=True, verbose_name="发布时间")
    content = models.TextField(verbose_name="内容")

    class Meta:
        ordering = ['-created_time']