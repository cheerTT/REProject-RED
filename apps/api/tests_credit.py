'''与小程序界面交互单元测试'''
# @Author : ttwen
# @Time   : 2019/3/15 15:28
# @Remark :  与小程序界面交互单元测试

import re
from django.test import TestCase  # 导入Django测试包
from django.template.loader import render_to_string

from api.models import Member, Credit
from commodity.models import CommodityType, Commodity
from apps.users.models import UserProfile
import datetime

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
                                   type=2, )

        self.login_user = {'username': 'cheertt', 'password': '123456'}

        Credit.objects.create(id=555,
                              behave='0',
                              creditpoints='2',
                              credittype='1',
                              createtime=datetime.datetime.now(),
                              userid=66
                                 )

    def test_CreditListView_get(self):
        """
        点击积分之后显示该用户积分详情的单元测试
        若返回200状态码，表示可以登陆页面可以正常显示
        否则，系统BUG,需要检查修复
        :return:
        """
        # 没登陆时候的状态
        credit = Credit.objects.all()

        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/credit/credit/list', dict(data=list(credit)))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_ShareView_post(self):
        """
        分享商品加积分
        :return:
        """
        idd = {'id': 6666}
        response = self.client.post('/share/', data=self.login_user)
        response = self.client.get('/member/credit/credit_share', idd)
        self.assertEqual(response.status_code, 200)

