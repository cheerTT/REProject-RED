# '''
# @Author:ttwen
# @Time:2019年3月7日10:45:35
# @Description: 会员管理的models层
# '''
#
#
# from django.db import models
#
# class ApiMember(models.Model):
#
#     ApiMember_type = (
#         ('0', '普通用户'),  # 已经通过微信小程序登录注册但没有人脸信息
#         ('1', '高级用户'),  # 已经通过微信小程序注册且有人脸信息
#     )
#
#     ApiMember_State = (
#         ('0', '正常'),  # 正常状态
#         ('1', '锁定'),  # 由于不正常操作导致用户被锁定，一定时间后可解锁
#     )
#
#     ApiMember_gender = (
#         ('0', '女'),
#         ('1', '男'),
#     )
#
#     openid = models.CharField(max_length=100, blank=True, null=True, verbose_name="openid")
#     face_json = models.TextField(blank=True, null=True, verbose_name="人脸信息")
#     pic_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="人脸图片位置")
#     nickname = models.CharField(max_length=20, verbose_name="昵称")
#     gender = models.CharField(max_length=4, choices=ApiMember_gender, default='0', verbose_name="性别")
#     avator = models.ImageField(upload_to="avator/%Y/%m", default="avator/default.jpg", max_length=100, null=True, blank=True)
#     city = models.CharField(max_length=20, verbose_name="城市")
#     province = models.CharField(max_length=20, verbose_name="省份")
#     type = models.CharField(choices=ApiMember_type, max_length=4, default="0", verbose_name="用户类型")
#     state = models.CharField(choices=ApiMember_State, max_length=4, default="0", verbose_name="用户状态")
#     last_login_date = models.DateField(blank=True, null=True, verbose_name="上次登录时间")
#     faceid = models.CharField(max_length=128, blank=True, null=True, verbose_name="faceid")
#     joined_date1 = models.DateField(blank=True, null=True, verbose_name="人脸录入时间")
#     joined_date2 = models.DateField(blank=True, null=True, verbose_name="用户注册时间")
#
#     class Meta:
#         verbose_name = "会员基本信息"
#         verbose_name_plural = verbose_name
#         ordering = ['id']
#         managed = False
#         db_table = 'api_member'
#
#         def __str__(self):
#             return self.nickname
#
#     class Remark(models.Model):
#         """
#         评论表的相对信息
#         """
#         pass
#
#
# # python manage.py inspectdb
#
#
