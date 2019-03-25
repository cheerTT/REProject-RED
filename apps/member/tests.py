'''
@Author:ttwen
@Time:2019年3月7日10:45:35
@Description: 会员管理的test方法
'''

import re
from django.test import TestCase  # 导入Django测试包
from django.template.loader import render_to_string

from api.models import Member
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

        Commodity.objects.create(openid='ABCDEFG',
                                 faceid='123',
                                 face_json='0.1,0.1',
                                 pic_name='1.jpg',
                                 joined_date1=datetime.datetime.now(),
                                 joined_date2=datetime.datetime.now(),
                                 nickname='123',
                                 gender='1',
                                 avatarUrl='http://1.jpg',
                                 city='chuzhou',
                                 province='anhui',
                                 state='0',
                                 codeVerify='123m',
                                 type='0',
                                 last_login_date=datetime.datetime.now()
                                 )

    def test_MemberView_get(self):
        """
        会员管理首页，显示会员列表页面
        :return:
        """
        response = self.client.post('/login/', data=self.login_user)
        expected_html = render_to_string('member/member_list.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        print(expected_html)

    def test_MemberListView_get(self):
        """
        点击会员管理之后商品列表显示的单元测试
        若返回200状态码，表示可以登陆页面可以正常显示
        否则，系统BUG,需要检查修复
        :return:
        """
        # 没登陆时候的状态
        member = Member.objects.all()

        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/member/member/list', dict(data=list(member)))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_MemberDetailView_get(self):
        """
        查看会员详情
        :return:
        """
        idd = {'id': 6666}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/member/member/detail', idd)

        self.assertEqual(response.status_code, 200)

    def test_MemberEnableView_post(self):
        '''
        启用用户
        :return:
        '''
        data = {'openid':'ABCDEFG',
                'faceid':'123',
                'face_json':'0.1,0.1',
                'pic_name':'1.jpg',
                'joined_date1':datetime.datetime.now(),
                'joined_date2':datetime.datetime.now(),
                'nickname':'123',
                'gender':'1',
                'avatarUrl':'http://1.jpg',
                'city':'chuzhou',
                'province':'anhui',
                'state':'1',
                'codeVerify':'123m',
                'type':'0',
                'last_login_date':datetime.datetime.now()}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/mmeber/member/enable', data=data)
        self.assertEqual(response.status_code, 200)

    def test_MemberEnableView_post(self):
        '''
        锁定用户
        :return:
        '''
        data = {'openid': 'ABCDEFG',
                'faceid': '123',
                'face_json': '0.1,0.1',
                'pic_name': '1.jpg',
                'joined_date1': datetime.datetime.now(),
                'joined_date2': datetime.datetime.now(),
                'nickname': '123',
                'gender': '1',
                'avatarUrl': 'http://1.jpg',
                'city': 'chuzhou',
                'province': 'anhui',
                'state': '0',
                'codeVerify': '123m',
                'type': '0',
                'last_login_date': datetime.datetime.now()}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/mmeber/member/disable', data=data)
        self.assertEqual(response.status_code, 200)
