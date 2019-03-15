# @Author  : cheertt
# @Time    : 2019/3/14 9:44
# @Remark  : 测试用户信息

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
        self.assertEqual(response.status_code, 200)

    def test_loginView_get(self):
        """
        登陆主界面单元测试
        若返回200状态码，表示可以登陆页面可以正常显示
        否则，系统BUG,需要检查修复
        :return:
        """
        # 没登陆时候的状态
        # response = self.client.get('/login/')
        # self.assertEqual(response.status_code, 200)

        # 登陆时候的状态，需要加上csrf验证
        response = self.client.post('/login/')
        expected_html = render_to_string('personal/personal_index.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        print(expected_html)

    def test_loginView_post(self):
        """
        测试用户登陆是否成功的状态，分如下四种测试用例
        1-登陆成功的情况；
        2-用户名或者密码错误的情况；
        3-用户名和密码不能够为空的情况；
        4-用户未激活的情况；
        :return:
        """
        # 若验证过期，可以加上下面这句
        response = self.client.post('/login/', data=self.login_user)
        # 1 因为我们的登陆实现了跳转，所以302就代表这成功登陆
        self.assertEqual(response.status_code, 302)
        # 2 若用户名或者密码错误，状态码为200且为True
        login_user1 = {'username': 'cheertt', 'password': '1223456'}
        response = self.client.post('/login/', data=login_user1)
        print('用户名或密码错误！' in response.content.decode())
        self.assertEqual(response.status_code, 200)
        # 3 若用户名或密码为空，状态吗为200且为True
        login_user2 = {'username': '', 'password': '1223456'}
        login_user3 = {'username': 'cheertt', 'password': ''}
        response = self.client.post('/login/', data=login_user2)
        print('用户名和密码不能够为空！' in response.content.decode())
        self.assertEqual(response.status_code, 200)
        # 4 若未绑定，状态码为200且为True
        response = self.client.post('/login/', data=self.login_user)
        print('用户未激活！' in response.content.decode())
        self.assertEqual(response.status_code, 200)

    def test_userListView_get(self):
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/users/user/list')
        print(response.content)
        # 成功返回符合条件的数据
        # b'{"data": [{"id": 1, "name": "python1234", "mobile": "15189392222", "email": "1913278504@qq.com", "url": "",
        # "is_active": true}]}'

    def test_userCreateView_post(self):
        # 拼接的错误的json格式
        user_add = {'csrfmiddlewaretoken': 'BH7xwbdI3V7HDGE6wXOkVfKy4pTf1VGFC2rktPex9sJprSCXWYYIENwcvLT4Ss3Y',
                    'name': 'test111',
                    'username': 'test111',
                    'is_active': 1,
                    'password': '111111',
                    'mobile': '15189392393',
                    'email': '3123@qq.com',
                    'joined_date': '2018-3-1',
                    'url': '1111'}
        # response = self.client.post('/login/', data=self.login_user)
        # response = self.client.post('/users/user/create', data=user_add)
        # print(response.status_code)
        # print(response.content)
        # 200
        # b'{"status": "fail", "user_create_form_errors": "\\u786e\\u8ba4\\u5bc6\\u7801\\u4e0d\\u80fd\\u4e3a\\u7a7a"}'
        # 拼接的正确的json格式
        user_add = {'csrfmiddlewaretoken': 'BH7xwbdI3V7HDGE6wXOkVfKy4pTf1VGFC2rktPex9sJprSCXWYYIENwcvLT4Ss3Y',
                    'name': 'test111',
                    'username': 'test111',
                    'is_active': 1,
                    'password': '111111',
                    'confirm_password': '111111',
                    'mobile': '15189392393',
                    'email': '3123@qq.com',
                    'joined_date': '2018-3-1',
                    'url': '1111'}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/users/user/create', data=user_add)
        print(response.status_code)
        print(response.content)
        # 200
        # b'{"status": "success"}'

    def test_userEnableView_post(self):
        idd = {'id': 1}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/users/user/enable', data=idd)
        print(response.status_code)
        print(response.content)
        # 200
        # b'{"result": "True"}'

    def test_userDisableView_post(self):
        idd = {'id': 1}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/users/user/disable', data=idd)
        print(response.status_code)
        print(response.content)
        # 200
        # b'{"result": "True"}'

    def test_userDeleteView_post(self):
        idd = {'id': 1}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/users/user/delete', data=idd)
        print(response.status_code)
        print(response.content)
        # 200
        # b'{"result": "true", "message": "\\u6570\\u636e\\u5220\\u9664\\u6210\\u529f\\uff01"}'
