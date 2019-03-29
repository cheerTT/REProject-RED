# @Time    : ${3/10/2019} ${TIME}
# @Author  : $Sutrue
# @Remark  :

from django.db import models

# Create your models here.

# class Commendation(models.Model):
#     assin = models.CharField(max_length=100, blank=False, null=False)
#     title = models.CharField(max_length=200, blank=True, null=True)
#     type = models.CharField(max_length=20, blank=True, null=True)
#
#     class Meta:
#         db_table = 'commendation'


class hot_list(models.Model):
    """
    热销表单model
    """
    assin = models.CharField(max_length=200, blank=False, null=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    categories = models.CharField(max_length=20, blank=True, null=True)
    sales_count = models.CharField(max_length=100, blank=True, null=True)
    present_price = models.CharField(max_length=200, blank=True, null=True)
    imUrl = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        """
        指定该类的数据库表单名字
        """
        db_table = 'hot_list'

class transaction_record(models.Model):
    """
    交易记录model
    """
    # id = models.IntegerField()
    user_id = models.CharField(max_length=255, blank=False, null=False)
    assin = models.CharField(max_length=255, blank=False, null=False)
    rating = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(max_length=255, blank=False, null=False)

    class Meta:
        """
        指定该类的数据库表单名字
        """
        db_table = 'transaction_record'
