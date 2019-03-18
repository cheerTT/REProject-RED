from django.db import models
from api.models import Member
from commodity.models import Commodity


# Create your models here.
class Transaction(models.Model):

    rating = models.IntegerField(default=3, blank=True, null=True, verbose_name="评分")
    num = models.IntegerField(default=0, blank=True, null=True, verbose_name="数量")
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="顾客")
    commodity = models.ForeignKey(Commodity, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="商品")
    orderid = models.CharField(max_length=32, default="", verbose_name="订单编号")
    joined_date = models.DateTimeField(null=True, blank=True, verbose_name="创建日期")

    class Meta:
        verbose_name = "订单表"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    def __str__(self):
        return self.id
