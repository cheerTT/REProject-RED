# @Time    : 2019/3/6 20:00
# @Author  : Virus
# @Remark  :


import re
from django.test import TestCase
from apps.users.models import UserProfile
from django.template.loader import render_to_string


class UserViewTest(TestCase):

# Create your tests here.

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
    def test_RecommendationsView_get(self):
        """
        测试是否成功转入recommendations页面
        若返回200状态码，表示可以进入recommendations页面可以正常显示
        否则系统bug，需要修复
        :return:
        """
        response = self.client.post('/login/')
        expected_html = render_to_string('recommendations/recommendations_list.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        self.assertEqual(response.status_code, 200)
        #print(expected_html)

    def test_RecommendationsDetailView_get(self):
            """
            登陆recommendationsDetail单元测试
            若返回200状态码，表示可以登陆页面可以正常显示
            否则，系统BUG,需要检查修复
            :return:
            """
            data = {'user_id': '45',
                    }
            response = self.client.post('/login/', data=self.login_user)
            response = self.client.get('/recommendations/recommendations/detail', data)
            print(response.content)
            self.assertEqual(response.status_code, 200)


    def test_RecommendationsListView_get(self):
        """
            登陆recommendationslist单元测试
            若返回200状态码，表示可以登陆页面可以正常显示
            否则，系统BUG,需要检查修复
        :return:
        """
        response = self.client.post('/login/')
        expected_html = render_to_string('recommendations/recommendations_list.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        self.assertEqual(response.status_code, 200)
        #print(expected_html)