# @Time    : 2019/3/17 10:44
# @Author  : Sutrue
# @Remark  : 测试手动推荐功能


from django.test import TestCase
from hotcommend.models import transaction_record, hot_list
from apps.users.models import UserProfile
from django.template.loader import render_to_string
import re
class HotCommendViewTest(TestCase):
    """
    测试是否成功转入hot_list页面
    :return
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

        hot_list.objects.create(id=6666,
                                assin='ABCDE12345',
                                present_price=1,
                                title='test',
                                categories=1,
                                sales_count=250,
                                )

        transaction_record.objects.create(
                                 assin='ABCDE12345',
                                 user_id=1234456,
                                 rating=5,
                                 id=777,
                                 date='2008-05-31 08:00:00',
        )

    def test_CommendView_get(self):
        """
        测试是否成功转入hot_list页面
        若返回200状态码，表示可以进入hot_list页面可以正常显示
        否则系统bug，需要修复
        :return:
        """
        response = self.client.post('/login/')
        expected_html = render_to_string('hotcommend/hot_list.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        self.assertEqual(response.status_code, 200)
        # print(expected_html)

    def test_ItemRank_get(self):
        """
        测试是否从数据库中获取到热销商品
        :return:
        """
        hot_commodity = transaction_record.objects.all()

        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/hotcommend/hotcommend/item_rank', dict(data=list(hot_commodity)))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_AddCommendation_get(self):
        """
        测试是否进入热销排名页面
        若返回200状态码，表示可以进入hot_list页面可以正常显示
        否则系统bug，需要修复
        :return:
        """
        response = self.client.post('/login/')
        expected_html = render_to_string('hotcommend/item_rank.html')
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        expected_html = re.sub(csrf_regex, '', expected_html)
        print(expected_html)

    def test_HotAdd_get(self):
        """
        测试是否从数据库中获取了当前手动推荐商品列表
        :return:
        """
        hotcommodity_list = hot_list.objects.all()

        response = self.client.post('/login/', data=self.login_user)
        response = self.client.get('/hotcommend/hotcommend/hot_list', dict(data=list(hotcommodity_list)))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_ToTheList_post(self):
        """
        测试是否成功将商品加入热门商品数据表
        :return:
        """
        commodity_id = {
            'assin': 'B00005JIVI',
        }
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/hotcommend/hotcommend/to_hot_list', data=commodity_id)
        self.assertEqual(response.status_code, 200)

    def test_HotDeleteView_post(self):
        """
        测试是否成功将物品从热销商品表中删除
        :return:
        """
        commodity_id = {
            'assin': 'B00005JIVI',
        }
        response = self.client.post('/login/', data=self.login_user)
        response = self.client.post('/hotcommend/hotcommend/hot_delete', data=commodity_id)
        self.assertEqual(response.status_code, 200)
