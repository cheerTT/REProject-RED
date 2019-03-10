# @Time    : ${3/10/2019} ${TIME}
# @Author  : $Sutrue
# @Remark  : 视图函数
from django.shortcuts import render
import json
import re

from django.shortcuts import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from commodity.models import Commodity, CommodityType
from django.core.serializers.json import DjangoJSONEncoder
from hotcommend.models import hot_list, transaction_record

from django.db.models import Count

class CommendView(LoginRequiredMixin, View):
    """
    转入热门推荐页
    """
    def get(self, request):
        return render(request, 'hotcommend/hot_list.html')


#通过QuerySet的values方法来获取指定字段列的数据内容，转换QuerySet类型最终序列化成json串，返回数据访问接口
class ItemRank(LoginRequiredMixin, View):
    """
    统计商品销量
    """
    def get(self, request):
        ret = transaction_record.objects.all().values('item_id').annotate(counts=Count('date')).order_by('-counts')
        #为每个物品添加对应的id
        # for item in ret:
        #     a = Commodity.objects.filter(assin=item['item_id'])
        #
        #     try:
        #         item['id'] = a.values('id')[0]['id']
        #     except IndexError:
        #         print("don't found: ", item['item_id'])
        ret = dict(data=list(ret))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')

class AddCommendation(LoginRequiredMixin, View):
    """
    进入热门推荐增加页面
    """
    def get(self, request):
        return render(request, 'hotcommend/item_rank.html')


class HotAdd(LoginRequiredMixin, View):
    """
    显示热门推荐列表
    """
    def get(self, request):
        fields = ['assin', 'title', 'categories']
        filters = dict()
        if 'assin' in request.GET and request.GET['assin']:
            filters['assin__icontains'] = request.GET['assin']
        if 'title' in request.GET and request.GET['title']:
            filters['title__icontains'] = request.GET['title']
        if 'categories' in request.GET and request.GET['categories']:
            filters['categories'] = request.GET['categories']
            # print(a.values('assin')[0]['assin'])
            # hot_commodity = hot_list(assin=a.values('assin')[0][')
        ret = dict(data=list(hot_list.objects.filter(**filters).values(*fields)))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        # if 'item_id' in request.POST and request.POST['item_id']:
        #     a = Commodity.objects.filter(assin=request.POST['item_id']).values(*fields)
        #     commodity = hot_list(assin=a.values('assin')[0]['assin'], title=a.values('title')[0]['title'], type=a.values('categories')[0]['categories'])
        #     commodity.save()
        return HttpResponse(ret, content_type='application/json')

class ToTheList(LoginRequiredMixin, View):
    """
    将选择的商品加入热门商品数据库
    """
    def post(self, request):
        ret=dict()
        fields = ['assin', 'title', 'categories']
        if 'item_id' in request.POST and request.POST['item_id']:
            a = Commodity.objects.filter(assin=request.POST['item_id']).values(*fields)

            #如果hot表中已经存在该商品，则不再放入
            if hot_list.objects.filter(assin=a.values('assin')[0]['assin']).count() == 0:
                hot_commodity = hot_list(assin=a.values('assin')[0]['assin'], title=a.values('title')[0]['title'], categories=a.values('categories')[0]['categories'])
                hot_commodity.save()
        return HttpResponse(ret, content_type='application/json')

class HotDeleteView(LoginRequiredMixin, View):
    """
    热门推荐商品删除视图
    """
    def post(self, request):

        ret = dict(result=False)
        if 'assin' in request.POST and request.POST['assin']:
            delete_item = request.POST.get('assin')
            hot_list.objects.filter(assin=delete_item).delete()

        ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


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
