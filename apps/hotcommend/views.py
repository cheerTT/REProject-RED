from django.shortcuts import render
import json
import re

from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from commodity.models import Commodity, CommodityType
from django.core.serializers.json import DjangoJSONEncoder
from hotcommend.forms import SalesQueryForm
from hotcommend.models import Sales_Counts, transaction_record

from django.db.models import Count

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
        return render(request, 'hotcommend/hotcommend.html', ret)


#通过QuerySet的values方法来获取指定字段列的数据内容，转换QuerySet类型最终序列化成json串，返回数据访问接口
class ItemRank(LoginRequiredMixin, View):
    def get(self, request):
        # fields = ['user_id', 'item_id',]
        filters = dict()
        # if 'user_id' in request.GET and request.GET['user_id']:
        #     filters['user_id'] = request.GET['user_id']
        # if 'item_id' in request.GET and request.GET['item_id']:
        #     filters['item_id'] = request.GET['item_id']
        # if 'rating' in request.GET and request.GET['rating']:
        #     filters['rating'] = request.GET['rating']
        # if 'date' in request.GET and request.GET['date']:
        #     filters['date'] = request.GET['date']
        ret = dict(data=list(transaction_record.objects.all().values('item_id').annotate(counts=Count('date')).order_by('-counts')))
        # ret['records']=records
        # ret = dict(data = list(ret))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        # return render(request, 'hotcommend/add_commendation.html')
        return HttpResponse(ret, content_type='application/json')

class AddCommendation(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        ret['status_list'] = "status_list"
        return render(request, 'hotcommend/item_rank.html')

# class SalesQuery(LoginRequiredMixin, View):
#     #查询近几日的销量
#
#     def get(self, request):
#         ret = dict()
#         fields = ['user_id', 'item_id', 'rating', 'date']
#         filters = dict()
#         if 'user_id' in request.GET and request.GET['user_id']:
#             filters['user_id'] = request.GET['user_id']
#         if 'item_id' in request.GET and request.GET['item_id']:
#             filters['item_id'] = request.GET['item_id']
#         if 'rating' in request.GET and request.GET['rating']:
#             filters['rating'] = request.GET['rating']
#         if 'date' in request.GET and request.GET['date']:
#             filters['date'] = request.GET['date']
#         records=transaction_record.objects.all().values('item_id').annotate(counts=Count('date')).order_by('-counts')
#         # ret = dict(data=list(transaction_record.objects.all().values('item_id').annotate(counts=Count('date')).order_by('-counts')))
#         # ret['commodity_types'] = CommodityType.objects.all()
#         print(records)
#         ret['records']=records
#         ret = json.dumps(ret, cls=DjangoJSONEncoder)
#         # return render(request, 'hotcommend/add_commendation.html')
#         return HttpResponse(ret, content_type='application/json')

    # def post(self, request):
    #     res = dict()
    #     sales_query_form = SalesQueryForm(request.POST)
    #     if sales_query_form.is_valid():
    #         sales_query_form.save()
    #         res['status'] = 'success'
    #     else:
    #         pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
    #         errors = str(sales_query_form.errors)
    #         sales_query_form_errors = re.findall(pattern, errors)
    #         res = {
    #             'status': 'fail',
    #             'sales_query_form_errors': sales_query_form_errors[0]
    #         }
    #     return HttpResponse(json.dumps(res), content_type='application/json')
