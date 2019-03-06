from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户: makemigration提示错误：sers.UserProfile.user_permissions: (fields.E304)，
    需要在settings中指定自定义认证模型：AUTH_USER_MODEL = 'users.UserProfile'
    """

    type_choices = (("0", "超级管理员"), ("1", "分配部门"), ("2", "商家"))

    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    # birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    # gender = models.CharField(max_length=10, choices=(("male", "男"), ("famale", "女")), default="male",
    #                           verbose_name="性别")
    mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    email = models.EmailField(max_length=100, verbose_name="邮箱")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.jpg", max_length=100, null=True,
                              blank=True)
    type = models.CharField(max_length=20, choices=type_choices, default="2", verbose_name="类型")
    # department = models.ForeignKey("Structure", null=True, blank=True, verbose_name="部门")
    # post = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    # superior = models.ForeignKey("self", null=True, blank=True, verbose_name="上级主管")
    # roles = models.ManyToManyField("rbac.Role", verbose_name="角色", blank=True)
    url = models.CharField(max_length=100, default="", verbose_name="摄像头路径")
    joined_date = models.DateField(null=True, blank=True, verbose_name="入职日期")

    class Meta:
        verbose_name = "商家信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
