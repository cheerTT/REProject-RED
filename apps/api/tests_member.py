# @Author : cheertt
# @Time   : 2019/3/15 15:28
# @Remark :  与小程序界面交互单元测试

import re
from django.test import TestCase  #导入Django测试包
from django.template.loader import render_to_string
from apps.users.models import UserProfile


class UserViewTest(TestCase):

    def setUp(self):
        """
        创建一条用户信息数据
        :return: None
        """
        UserProfile.objects.create(id=1,
                                   password='pbkdf2_sha256$36000$4cg1SAMlOhxd$ONEWDCYTR/kbWBuwpMIo1GUJvMsC+cHZgFUl9YF6KC0=',
                                   is_superuser=1,
                                   username='cheertt',
                                   first_name='cheertt',
                                   last_name='油炸皮卡丘',
                                   email='1913278504@qq.com',
                                   is_staff=1,
                                   is_active=1,
                                   date_joined='2019-03-01 14:56:48.298648',
                                   name='python1234',
                                   mobile='15189392222',
                                   type=2,)

        self.login_user = {'username': 'cheertt', 'password': '123456'}

    def test_indexView_get(self):
        """
        自动条状登陆之后首页的单元测试
        若返回302的状态码，由于拦截器的缘故，用户没有登陆导致
        若返回200的状态吗，则表示管理员正确登陆，进入后台管理页面
        :return:
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
