# @Time    : 2019年3月5日19:54:50
# @Author  : xie Liangcai
# @Remark  : 商品种类，信息，价格model


from django.db import models



# 商品类别表
class CommodityType(models.Model):
    '''
    商品类型model
    '''
    type_name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "commodity_type"


# 商品列表
class Commodity(models.Model):
    '''
       商品信息model
    '''
    commodity_status = (
        ("0", "下架"),
        ("1", "在售"),
    )
    assin = models.CharField(max_length=100, blank=False, null=False)
    categories = models.ForeignKey(CommodityType, on_delete=models.SET_NULL, blank=True, null=True)
    present_price = models.FloatField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    # imUrl = models.ImageField(upload_to="commImage",default="commImage/default.jpg")
    imUrl = models.CharField(max_length=1000, blank=True, null=True)
    brand = models.CharField(max_length=1000, blank=True, null=True)
    buyDate = models.DateTimeField('商品购买日期', blank=True, null=True)
    warrantyDate = models.DateTimeField('商品保质日期', blank=True, null=True)
    status = models.CharField(choices=commodity_status, max_length=20, default="1", verbose_name="商品的状态")


    def short_description(self):
        if len(str(self.description)) > 400:
            return '{}...'.format(str(self.description)[0:400])
        else:
            return str(self.description)

    def short_title(self):

        if len(str(self.title)) > 50:
            return '{}...'.format(str(self.title)[0:50])
        else:
            return str(self.title)
    class Meta:
        db_table = "commodity"


# 商品价格表
class Commodity_price(models.Model):
    '''
       商品价格model
    '''
    asin = models.ForeignKey(Commodity)
    price = models.FloatField(default=0, blank=True)
    updataTime = models.DateTimeField('价格更新日期', auto_now_add=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "commodity_price"
