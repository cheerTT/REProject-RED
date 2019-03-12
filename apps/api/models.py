from django.db import models


class Member(models.Model):
    gender_choices = (('1', '男'), ('2', '女'))
    state_choices = (('0', '正常'), ('1', '锁定'))
    type_choices = (('0', '普通用户'), ('1', '高级用户'))

    openid = models.CharField(max_length=100, null=True, blank=True, verbose_name="openid")
    faceid = models.CharField(max_length=128, null=True, blank=True, verbose_name="faceid")
    face_json = models.TextField(null=True, blank=True, verbose_name="人脸信息")
    pic_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="人脸图片位置")
    joined_date1 = models.DateField(null=True, blank=True, verbose_name="人脸录入时间")
    joined_date2 = models.DateField(null=True, blank=True, verbose_name="用户注册时间")

    nickname = models.CharField(max_length=20, verbose_name="昵称")
    gender = models.CharField(max_length=4, choices=gender_choices, default='1', verbose_name="性别")
    avatarUrl = models.CharField(max_length=200, verbose_name="头像链接", null=True, blank=True)
    city = models.CharField(max_length=20, verbose_name="城市")
    province = models.CharField(max_length=20, verbose_name="省份")
    state = models.CharField(max_length=4, choices=state_choices, default='0', verbose_name="会员状态")
    codeVerify = models.CharField(max_length=6, verbose_name="验证码", default='-1')
    type = models.CharField(max_length=4, choices=type_choices, default='0', verbose_name="会员级别")
    last_login_date = models.DateTimeField(null=True, blank=True, verbose_name="上次登录时间")

    class Meta:
        verbose_name = "会员基本信息"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    def __str__(self):
        return self.nickname


class Remark(models.Model):
    """
    评论表的相对信息
    """
    pass
