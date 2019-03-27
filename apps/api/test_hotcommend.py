from django.test import TestCase  # 导入Django测试包
from django.template.loader import render_to_string

from hotcommend.models import hot_list
from django.core.paginator import Paginator


class UserViewTest(TestCase):

    def setUp(self):
        """
               创建一条用户信息数据
               :return: None
               """

        hot_list.objects.create(assin='sutrue_test_assin',
                                title='sutrue_test_title',
                                categories='sutrue_test_type',
                                sales_count=10,
                                present_price=15.5,
                                imUrl='sutrue_test_imUrl')


    def test_HotCommodityView_get(self):
        """
        小程序端获得热销商品数据
        :param self:
        :return:
        """
        hot_commodity = hot_list.objects.all()
        response = self.client.get('/api/hotcommend/hot_commodity', dict(data=list(hot_commodity), p=1))
        print(response.content)
        self.assertEqual(response.status_code, 200)

