# @Time    : 2019/3/12 17:41
# @Author  : Sutrue
# @Remark  : 热门推荐接口

import json
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
# from django.views.decorators.csrf import csrf_exempt
from api.models import Member
from commodity.models import Commodity
from hotcommend.models import hot_list
from django.core.paginator import Paginator
from hotcommend.models import hot_list

class HotCommodityView(View):
    def get(self, request):

        fields = ['id', 'assin', 'title', 'categories', 'present_price', 'sales_count', 'imUrl']
        filters = dict()
        # if 'commodity_id' in request.GET and request.GET['commodity_id']:
        #     filters['categories'] = request.GET['commodity_id']
        # if 'mix_kw' in request.GET and request.GET['mix_kw']:
        #     filters['title__icontains'] = request.GET['title']

        p = int(request.GET['p'])
        page_size = 10

        hot_commodity = hot_list.objects.values(*fields).order_by("id")

        paginator = Paginator(hot_commodity, page_size)
        print("hottttttttttttttttttttttt")

        hot_commodity_pages = paginator.page(p)   #第p页的内容
        # # print("是否有下一页：",commodity_pages.has_next())
        ret = dict(data=list(hot_commodity_pages))
        ret["has_more"] = hot_commodity_pages.has_next()  #是否有下一页
        # ret = dict(data=list(hot_commodity))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        # print("ret:",ret)
        return HttpResponse(ret, content_type='application/json')