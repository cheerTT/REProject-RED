# @Time    : 2019/3/25 16:46
# @Author  : xie Liangcai
# @Remark  :


import re
from django.test import TestCase  # 导入Django测试包
from django.template.loader import render_to_string

from api.models import Member, Cart
from apps.comment.models import Comment
from commodity.models import CommodityType, Commodity
from apps.users.models import UserProfile


class UserViewTest(TestCase):

    def setUp(self):
        """
               创建一条用户信息数据
               :return: None
               """

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
        CommodityType.objects.create(id=1, type_name="Baby")
        Member.objects.create(id=1, )
        Comment.objects.create(id=1, content="test", commodity_id=6666, joined_date='2019-03-20 19:16:45.316348',
                               member_id=1)
        Cart.objects.create(id=1, commodity_id=6666, member_id=1)

    def test_CommoditySearchView_get(self):
        """
        收银页面查找商品测试

        :return:
        """
        data = {'s': 'ABCDE12345'}
        response = self.client.get('/api/commodity/search', data=data)
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_CommodityTypeView_get(self):
        """
        商品类别展示
        :return:
        """
        commodity_type = CommodityType.objects.all()
        response = self.client.get('/api/commodity/list', dict(data=list(commodity_type)))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_CommodityListView_get(self):
        """
        小程序端商品列表展示
        :return:
        """
        data={'p':1}
        response = self.client.get('/api/commodity/commodity_list',data=data)
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_CommodityInfoView_post(self):
        """
        查看商品详情
        :return:
        """

        response = self.client.post('/api/commodity/commodity_info')
        self.assertEqual(response.status_code, 200)

    def test_CommodityCommentsView_get(self):
        """
        查看商品所有评论
        :return:
        """

        data={'id':6666}
        response = self.client.get('/api/commodity/commodity_comments', data=data)
        self.assertEqual(response.status_code, 200)

    def test_CommentAddView_post(self):
        """
        用户添加评论
        :return:
        """
        comment = {'id': 2,
                   'content': 'test2',
                   'joined_date': '2019-03-20 19:16:45.316348',
                   'commodity_id': 6666,
                   'member_id': 1
                   }
        response = self.client.post('/api/commodity/comment_add', data=comment)
        self.assertEqual(response.status_code, 200)


def test_CartAddView_post(self):
    '''
     加入收藏
    :return:
    '''
    data = {'id': 12,
            'commodity_id': 6666,
            'member_id': 1
            }
    response = self.client.post('/api/commodity/cart_add', data=data)
    self.assertEqual(response.status_code, 200)


def test_CartListView_post(self):
    '''
    显示该用户的所有收藏
    :return:
    '''
    data = {'member_id': 1, }
    response = self.client.post('/api/commodity/enable', data=data)
    self.assertEqual(response.status_code, 200)


def test_CartDeltView_post(self):
    '''
    删除收藏
    :return:
    '''
    goods = [1]
    response = self.client.post('/api/commodity/cart_del', data=goods)
    self.assertEqual(response.status_code, 200)
