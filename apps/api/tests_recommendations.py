# @Time    : 2019/3/27 9:24
# @Author  : 1234
# @Remark  :

import re
from django.test import TestCase  # 导入Django测试包
from apps.users.models import UserProfile
from utils.wechat_utils import WechatUtils

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

    def test_TopRecommendationsView_get(self):
        """
        顶部推荐的单元测试
        :return:
        """
        # 没登陆时候的状态
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/recommendations/toprecommendations')
        print(response.content)

    def test_Get_Common_Recommenadations_get(self):
        """
        用户画像推荐的单元测试
        :return:
        """
        # 没登陆时候的状态
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/recommendations/commonrecommendations')
        print(response.content)


    def test_AllRecommendationsView_get(self):
        """
        100个推荐列表的单元测试
        :return:
        """
        # 没登陆时候的状态
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/recommendations/allrecommendations')
        print(response.content)
