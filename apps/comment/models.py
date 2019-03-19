# @Author  : cheertt
# @Time    : 2019/3/19 8:04
# @Remark  : 收银界面以及小程序会员登陆注册与个人信息显示部分信息
from django.db import models
from api.models import Member
from commodity.models import Commodity


# Create your models here.
class Comment(models.Model):

    state_choices = (('0', '正常'), ('1', '锁定'))

    content = models.CharField(max_length=300, null=True, blank=True, verbose_name="评论内容", default="")
    joined_date = models.DateTimeField(null=True, blank=True, verbose_name="评论时间")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, verbose_name='评论人')
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=True, blank=True, verbose_name="评论商品")
    state = models.CharField(null=True, blank=True, max_length=4, choices=state_choices, default='0',
                             verbose_name="评论状态")
