# @Time    : 2019/3/12 17:41
# @Author  : Sutrue
# @Remark  : 热门推荐接口

import json
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from hotcommend.models import hot_list

class HotCommodityView(View):
    """
    将数据发送到小程序前端
    """
    def get(self, request):
        """
        返回hot_list表中数据
        :param request:
        :return:
        """
        fields = ['id', 'assin', 'title', 'categories', 'present_price', 'sales_count', 'imUrl']
        # filters = dict()
        # if 'commodity_id' in request.GET and request.GET['commodity_id']:
        #     filters['categories'] = request.GET['commodity_id']
        # if 'mix_kw' in request.GET and request.GET['mix_kw']:
        #     filters['title__icontains'] = request.GET['title']

        get_page = int(request.GET['p'])
        page_size = 10

        hot_commodity = hot_list.objects.values(*fields).order_by("id")

        paginator = Paginator(hot_commodity, page_size)
        # print("hottttttttttttttttttttttt")

        hot_commodity_pages = paginator.page(get_page)   #第p页的内容
        # # print("是否有下一页：",commodity_pages.has_next())
        ret = dict(data=list(hot_commodity_pages))
        ret["has_more"] = hot_commodity_pages.has_next()  #是否有下一页
        # print(ret)
        # ret = dict(data=list(hot_commodity))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        # print("ret:",ret)
        return HttpResponse(ret, content_type='application/json')