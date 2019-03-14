import re
from django.test import TestCase
from django.template.loader import render_to_string
from apps.users.models import UserProfile


class PersonalViewTest(TestCase):
    """
    个人信息相关的单元测试
    """
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

    def test_personalView_get(self):
        """
        显示个人信息，若登陆成功，则会在系统的工作台显示个人信息
        :return:
        """
        expected_html = render_to_string('personal/personal_index.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        print(expected_html)
        # 成功显示界面信息

    def test_userInfoView_post(self):
        """
        用户个人中心信息
        :return:
        """
        idd = {'id': '1'}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/personal/userinfo', data=idd)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        # b'{"status": "fail"}'

    def test_uploadImageView_post(self):
        """
        修改个人头像，修改成功后需要刷新页面，并将原来的头像直接覆盖
        在浏览器上测试通过
        :return:
        """
        pass

    def test_passwdChangeView_post(self):
        """
        修改密码-必须两次正确的密码，且保证两次输入的密码一致
        :return:
        """
        # pwd = {'password': '222222', 'confirm_password': '222222'}
        # response = self.client.post('/login/', data=self.login_user)
        # response = self.client.post('/personal/passwordchange', data=pwd)
        # self.assertEqual(response.status_code, 200)
        # print(response.content)
        # b'{"status": "success"}'
        pwd1 = {'password': '222222', 'confirm_password': '2122222'}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/personal/passwordchange', data=pwd1)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        # b'{"status": "fail", "admin_passwd_change_form_errors":
        # "\\u4e24\\u6b21\\u5bc6\\u7801\\u8f93\\u5165\\u4e0d\\u4e00\\u81f4"}'
