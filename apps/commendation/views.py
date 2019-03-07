from django.shortcuts import render
import json

from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponse
from django.contrib.auth import get_user_model
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from commendation.models import sales_counts
from commodity.models import Commodity, CommodityType
from django.core.serializers.json import DjangoJSONEncoder
import pandas as pd

class CommendView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        status_list = []
        for status in Commodity.commodity_status:
            status_dict = dict(item=status[0], value=status[1])
            status_list.append(status_dict)
        commodity_types = CommodityType.objects.all()
        ret['status_list'] = status_list
        ret['commodity_types'] = commodity_types
        return render(request, 'commendation/commendation.html', ret)


#通过QuerySet的values方法来获取指定字段列的数据内容，转换QuerySet类型最终序列化成json串，返回数据访问接口
class CommendListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'commendation/commendation_list.html')

class SalesQuery(LoginRequiredMixin, View):
    #查询近几日的销量

    def get(self, request):
        fields = ['id', 'assin', 'title', 'brand', 'status', 'buyDate', 'present_price', 'categories__type_name']
        filters = dict()
        if 'assin' in request.GET and request.GET['assin']:
            filters['assin__icontains'] = request.GET['assin']
        if 'title' in request.GET and request.GET['title']:
            filters['title__icontains'] = request.GET['title']
        if 'categories' in request.GET and request.GET['categories']:
            filters['categories'] = request.GET['categories']
        # if 'brand' in request.GET and request.GET['brand']:
        #     filters['brand__icontains'] = request.GET['brand']
        if 'status' in request.GET and request.GET['status']:
            filters['status'] = request.GET['status']
        ret = dict(data=list(Commodity.objects.filter(**filters).values(*fields)))

        ret = json.dumps(ret, cls=DjangoJSONEncoder)

        return render(request, 'commendation/sales_query.html')