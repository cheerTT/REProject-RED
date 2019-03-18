from django.db import models


class Member(models.Model):
    gender_choices = (('1', '男'), ('2', '女'))
    state_choices = (('0', '正常'), ('1', '锁定'))
    type_choices = (('0', '普通用户'), ('1', '高级用户'))

    openid = models.CharField(max_length=100, null=True, blank=True, verbose_name="openid", default=0)
    faceid = models.CharField(max_length=128, null=True, blank=True, verbose_name="faceid")
    face_json = models.TextField(null=True, blank=True, verbose_name="人脸信息")
    pic_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="人脸图片位置")
    joined_date1 = models.DateField(null=True, blank=True, verbose_name="人脸录入时间")
    joined_date2 = models.DateField(null=True, blank=True, verbose_name="用户注册时间", default='2019-01-01')

    nickname = models.CharField(null=True, blank=True,max_length=20, verbose_name="昵称", default='暂无')
    gender = models.CharField(null=True, blank=True,max_length=4, choices=gender_choices, verbose_name="性别", default='暂无')
    avatarUrl = models.CharField(max_length=200, verbose_name="头像链接", null=True, blank=True, default='暂无')
    city = models.CharField(null=True, blank=True,max_length=20, verbose_name="城市", default='暂无')
    province = models.CharField(null=True, blank=True,max_length=20, verbose_name="省份", default='暂无')
    state = models.CharField(null=True, blank=True,max_length=4, choices=state_choices, default='0', verbose_name="会员状态")
    codeVerify = models.CharField(null=True, blank=True,max_length=6, verbose_name="验证码", default='-1')
    type = models.CharField(null=True, blank=True,max_length=4, choices=type_choices, default='0', verbose_name="会员级别")
    last_login_date = models.DateTimeField(null=True, blank=True, verbose_name="上次登录时间", default='2019-01-01')

    # def null_nickname(self):
    #     if self.nickname ==  None:
    #         return '暂无'
    #     else:
    #         return str(self.nickname)
    #
    # def null_gender(self):
    #     if self.gender ==  None:
    #         return '暂无'
    #     else:
    #         return str(self.nickname)
    #
    # def null_city(self):
    #     if self.city ==  None:
    #         return '暂无'
    #     else:
    #         return str(self.nickname)
    #
    # def null_province(self):
    #     if self.province ==  None:
    #         return '暂无'
    #     else:
    #         return str(self.nickname)
    class Meta:
        verbose_name = "会员基本信息"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    # def __str__(self):
    #     return self.nickname


class Remark(models.Model):
    """
    评论表的相对信息
    """
    pass

class Credit(models.Model):

    '''
    0：每日首次登陆送积分：+2分/次
    1：消费送积分：+1分/元
    2：每日首次转发送积分：+3分/次
    3：发表评论送积分：+2分/条
    4：消费抵扣积分：-1元/100分
    '''
    type_choices = (('0', '收入'), ('1', '支出'))
    bahave_choices = (('0', '每日首次登陆加积分'),('1', '消费送积分'),('2', '转发送积分'),('3','发表评论送积分'),('4', '消费抵扣积分'))

    behave = models.CharField(null=True, blank=True, max_length=50, choices=bahave_choices, verbose_name='产生积分变动的行为')
    points = models.IntegerField(null=True, blank=True, verbose_name='每条行为对应的积分')
    type = models.CharField(null=True, blank=True, max_length=4, choices=type_choices, verbose_name='积分变动类型')
    createtime = models.DateTimeField(null=True, blank=True, verbose_name='积分变动时间')
    userid = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, verbose_name='产生积分变动的用户id')

    class Meta:
        verbose_name = "会员积分变动信息表"
        verbose_name_plural = verbose_name
        ordering = ["createtime"]
