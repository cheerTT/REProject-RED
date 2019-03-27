# @Time    : 2019年3月15日16:01:17
# @Author  : xie Liangcai
# @Remark  :


import re
from django.test import TestCase  # 导入Django测试包
from django.template.loader import render_to_string
from commodity.models import CommodityType, Commodity
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
                                   type=2, )

        self.login_user = {'username': 'cheertt', 'password': '123456'}

        Commodity.objects.create(id=6666,
                                 assin='ABCDE12345',
                                 present_price=1,
                                 description='This is a test data',
                                 title='test',
                                 categories_id=1,
                                 brand='test',
                                 status=1,
                                 buyDate='2019-3-15',
                                 warrantyDate='2020-3-15',
                                 )

    def test_CommodityView_get(self):
        """
        商品管理首页，显示商品列表页面

        :return:
        """
        response = self.client.post('/login/', data=self.login_user)
        expected_html = render_to_string('commodity/commodity_list.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        print(expected_html)

    def test_CommodityListView_get(self):
        """
        点击商品管理之后商品列表显示的单元测试
        若返回200状态码，表示可以登陆页面可以正常显示
        否则，系统BUG,需要检查修复
        :return:
        """
        # 没登陆时候的状态
        commodity = Commodity.objects.all()

        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/commodity/commodity/list', dict(data=list(commodity)))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_CommodityCreateView_get(self):
        """
        添加商品信息页面
        :return:
        """
        response = self.client.post('/login/', data=self.login_user)
        expected_html = render_to_string('commodity/commodity_create.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        print(expected_html)
        # idd={'id':6666}
        # response = self.client.post('/login/', data=self.login_user)
        # response = self.client.get('/commodity/commodity/detail', idd)
        # self.assertEqual(response.status_code, 200)

    def test_CommodityCreateView_post(self):
        """
        添加商品信息
        :return:
        """
        commodity_add = {
            'id': 7777,
            'assin': 'ABCDE4567',
            'present_price': 11,
            'description': 'This is a test data 2',
            'title': 'test',
            'categories_id': 1,
            'brand': 'test',
            'status': 1,
            'buyDate': '2019-3-15',
            'warrantyDate': '2020-3-15',

        }
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/commodity/commodity/create', data=commodity_add)
        # print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_CommodityUpdateView_get(self):
        """
        点击更新跳转商品更新信息页面
        :return:
        """
        commodity = Commodity.objects.filter(id=6666)
        response = self.client.post('/login/', data=self.login_user)
        expected_html = render_to_string('commodity/commodity_update.html', dict(data=list(commodity)))
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        print(expected_html)
        # 成功显示界面信息

    def test_CommodityUpdateView_post(self):
        """
        修改商品信息
        :return:
        """
        data = {'id': 6667,
                'assin': 'ABCDE12345',
                'present_price': 1,
                'description': 'This is a test data',
                'title': 'test',
                'categories_id': 1,
                'brand': 'test',
                'status': 1,
                'buyDate': '2019-3-15',
                'warrantyDate': '2020-3-15', }
        # idd = {"assin": 'ABCDE12345'}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/commodity/commodity/update', data=data)
        self.assertEqual(response.status_code, 200)

    def test_CommodityDeleteView_post(self):
        '''
         删除商品
        :return:
        '''
        data = {'id': 6667, }
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/commodity/commodity/delete', data=data)
        self.assertEqual(response.status_code, 200)

    def test_CommodityEnableView_post(self):
        '''
        上架商品
        :return:
        '''
        data = {'id': 6667, }
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/commodity/commodity/enable', data=data)
        self.assertEqual(response.status_code, 200)

    def test_CommodityDisableView_post(self):
        '''
        下架商品
        :return:
        '''
        data = {'id': 6667, }
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/commodity/commodity/diable', data=data)
        self.assertEqual(response.status_code, 200)

    def test_CommodityDetailView_get(self):
        """
        查看商品详情
        :return:
        """
        idd = {'id': 6666}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/commodity/commodity/detail', idd)

        self.assertEqual(response.status_code, 200)

    def test_UploadImageView_get(self):
        """
        添加商品信息
        :return:
        """
        idd = {'assin': '12345ABCDE', 'categories': 1}
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/commodity/commodity/uploadimage', idd)
        self.assertEqual(response.status_code, 200)

    def test_UploadImageView_post(self):
        """
        上传商品图片
        :return:
        """
        pass
