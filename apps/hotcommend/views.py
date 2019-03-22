# @Time    : ${3/10/2019} ${TIME}
# @Author  : $Sutrue
# @Remark  : 视图函数
from django.shortcuts import render
import json
from datetime import datetime, timedelta
import operator
import time
import re

from django.shortcuts import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from commodity.models import Commodity, CommodityType
from order.models import Transaction
from django.core.serializers.json import DjangoJSONEncoder
from hotcommend.models import hot_list, transaction_record

from django.db.models import Count, Sum, F
from django.utils.safestring import mark_safe
from itertools import chain

class CommendView(LoginRequiredMixin, View):
    """
    转入热门推荐页
    """
    def get(self, request):
        now_time = datetime.now().strftime('%Y-%m-%d')
        day_7_ago = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d')
        day_14_ago = (datetime.now() + timedelta(days=-14)).strftime('%Y-%m-%d')
        day_30_ago = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')
        ret = dict()
        # ret['rates'] = mark_safe(list(transaction_record.objects.all().filter(assin='B004E4CCSQ').values('date').annotate(sales_count=Count('id')).
        #                               filter(date__gte=day_30_ago, date__lte=now_time).order_by('date')))

        #最近一周的销量
        recent7 = transaction_record.objects.all().values('assin').annotate(sales_count=Count('id')).filter(date__gte='2013-02-26', date__lte='2013-03-11').order_by('date')
        recent14 = transaction_record.objects.all().values('assin').annotate(sales_count=Count('id')).filter(date__gte='2013-02-11', date__lte='2013-03-11').order_by('date')

        inc = {}
        for i in recent7:
            for j in recent14:
                if j['assin'] == i['assin']:
                    try:
                        inc[i['assin']] = i['sales_count'] / (j['sales_count'] - i['sales_count'])
                        # inc.append([j['assin'], i['sales_count'] / (j['sales_count'] - i['sales_count'])])
                    except ZeroDivisionError:
                        pass
                    break

        sortInc = sorted(inc, key=lambda x:inc[x], reverse=True)[:6]


        data = []
        # 根据日期进行循环
        begin = datetime.strptime("2013-02-11", "%Y-%m-%d")
        end = datetime.strptime("2013-03-12", "%Y-%m-%d")
        delta = timedelta(days=1)

        for assin in sortInc:
            data_sales = list(transaction_record.objects.all().filter(assin=assin).values('date').annotate(sales_count=Count('id')).
                                     filter(date__gte='2013-02-11', date__lte='2013-03-11'))
            aa = []
            #去除日期的时分秒
            for i in data_sales:
                short = i['date'][:10]
                aa.append(short)
                i['date'] = short

            #将没有销量的日期销量数定位0
            d = begin
            while d <= end:
                da = str(d.strftime("%Y-%m-%d"))
                if da not in aa:
                    data_sales.append({'date': da, 'sales_count':0})
                d += delta


            data_sales = sorted(data_sales, key=lambda x:x['date'])
            data.append([assin, data_sales])
        ret['rates'] = mark_safe(data)
        return render(request, 'hotcommend/hot_list.html', ret)


#通过QuerySet的values方法来获取指定字段列的数据内容，转换QuerySet类型最终序列化成json串，返回数据访问接口
class ItemRank(LoginRequiredMixin, View):
    """
    统计商品销量
    """
    def get(self, request):
        """
        按商品id统计指定时间内的商品销量，默认近7天的
        """

        now_time = datetime.now().strftime('%Y-%m-%d')
        day_3_ago = (datetime.now() + timedelta(days=-3)).strftime('%Y-%m-%d')
        day_7_ago = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d')
        day_30_ago = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')

        # choose_date = {'3': day_3_ago, '7': day_7_ago, '30': day_30_ago}

        #接收根据assin查询传来的assin值
        if 'assin' in request.GET and request.GET['assin']:
            ret = Commodity.objects.filter(assin=request.GET['assin']).annotate(commodity=F('id'), commodity__title=F('title')).values('commodity', 'commodity__title', 'status')


            status = '0'
            try:
                status = ret.values('status')[0]['status']
            except IndexError:
                pass

            #判断商品是否下架
            if status == '1':
                sales_count = Transaction.objects.all().filter(commodity__assin=request.GET['assin']).values('commodity__assin').annotate(sales_count=Sum('num')).filter(joined_date__gte=day_30_ago, joined_date__lte=now_time)
                count = 0
                try:
                    for item in sales_count:
                        count += item['sales_count']
                except IndexError:
                    count = 0
                    print("无销售记录")

                for item in ret:
                    # a = Commodity.objects.filter(assin=item['assin'])
                    item['sales_count'] = count
                ret = dict(data=list(ret))
                ret = json.dumps(ret, cls=DjangoJSONEncoder)
                return HttpResponse(ret, content_type='application/json')
            else:
                print("不存在")
                ret = dict()
                ret = json.dumps(ret, cls=DjangoJSONEncoder)
                return HttpResponse(ret, content_type='application/json')

        fields = ['commodity', 'orderid', 'joined_date', 'commodity__title']
        ret = Transaction.objects.all().values('commodity', 'commodity__title').annotate(sales_count=Sum('num')).filter(joined_date__gte=day_30_ago, joined_date__lte=now_time).order_by('-sales_count')[:50]

        # 为每个物品添加对应的title
        # for item in ret:
        #     a = Commodity.objects.filter(assin=item['assin'])
        #     # item['title'] = item['commodity'].
        #     try:
        #         item['title'] = a.values('title')[0]['title']
        #     except IndexError:
        #         print("don't found: ", item['assin'])

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
        fields = ['assin', 'title', 'sales_count', 'categories', 'id']
        filters = dict()
        if 'assin' in request.GET and request.GET['assin']:
            filters['assin__icontains'] = request.GET['assin']
        if 'title' in request.GET and request.GET['title']:
            filters['title__icontains'] = request.GET['title']
        if 'sales_count' in request.GET and request.GET['sales_count']:
            filters['sales_count'] = request.GET['sales_count']
        if 'categories' in request.GET and request.GET['categories']:
            filters['categories'] = request.GET['categories']
        if 'id' in request.GET and request.GET['id']:
            filters['id'] = request.GET['id']


        #将昨天销量前20的自动加入hot_list表中
        now_time = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
        yesterday_count = Transaction.objects.all().values('commodity', 'commodity__assin').annotate(counts=Sum('num')).filter(joined_date__gte=yesterday, joined_date__lte=now_time)[:20]
        for item in yesterday_count:
            if hot_list.objects.filter(assin=item['commodity__assin']).count() == 0:
                b = Commodity.objects.filter(assin=item['commodity__assin']).values('id', 'assin', 'title', 'categories', 'present_price', 'imUrl')
                hot_commodity = hot_list(assin=b.values('assin')[0]['assin'], title=b.values('title')[0]['title'],
                                         categories=b.values('categories')[0]['categories'], imUrl=b.values('imUrl')[0]['imUrl'],
                                         present_price=b.values('present_price')[0]['present_price'], sales_count=item['counts'], id=b.values('id')[0]['id'])
                hot_commodity.save()

        ret = dict(data=list(hot_list.objects.filter(**filters).values(*fields)))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)

        return HttpResponse(ret, content_type='application/json')


class ToTheList(LoginRequiredMixin, View):
    """
    将选择的商品加入热门商品数据库
    """
    def post(self, request):
        ret=dict()
        now_time = datetime.now().strftime('%Y-%m-%d')
        day_30_ago = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')
        fields = ['id', 'assin', 'title', 'categories', 'present_price', 'imUrl', 'status']

        #销量单独获取
        sales_count = Transaction.objects.all().filter(commodity=request.POST['commodity']).values('commodity').annotate(sales_count=Sum('num')).filter(joined_date__gte=day_30_ago, joined_date__lte=now_time)
        count = 0
        try:
            for item in sales_count:
                count += item['sales_count']
        except IndexError:
            count = 0


        a = Commodity.objects.filter(id=request.POST['commodity']).values(*fields)
        #如果hot表中已经存在该商品，则不再放入
        if a.values('status')[0]['status'] == '1':
            if hot_list.objects.filter(assin=a.values('assin')[0]['assin']).count() == 0:
                hot_commodity = hot_list(assin=a.values('assin')[0]['assin'], title=a.values('title')[0]['title'], categories=a.values('categories')[0]['categories'],
                                         imUrl=a.values('imUrl')[0]['imUrl'], present_price=a.values('present_price')[0]['present_price'],
                                         sales_count=count, id=a.values('id')[0]['id'])
                hot_commodity.save()
        return HttpResponse(ret, content_type='application/json')


class HotDeleteView(LoginRequiredMixin, View):
    """
    热门推荐商品删除视图
    """
    def post(self, request):

        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            delete_item = request.POST.get('id').split(',')
            hot_list.objects.filter(id__in=delete_item).delete()

        ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class IncreaseRateView(LoginRequiredMixin, View):
    def get(self, request):
        print(transaction_record.objects.all().values())


        ret = dict(data=list(transaction_record.objects.all().values()))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)

        return HttpResponse(ret, content_type='application/json')



# class ChooseDays(LoginRequiredMixin, View):
#     def get(self, request):
#         """
#         按商品id统计指定时间内的商品销量，默认近三天的
#         """
#         your_date = request.POST['date']
#
#         now_time = datetime.now().strftime('%Y-%m-%d')
#         day_3_ago = (datetime.now() + timedelta(days=-3)).strftime('%Y-%m-%d')
#         day_7_ago = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d')
#         day_30_ago = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')
#         choose_date = {'3': day_3_ago, '7':day_7_ago, '30':day_30_ago}
#         print(choose_date[your_date])
#
#
#         print(request.POST['date'])
#         # print(choose_date)
#         ret = transaction_record.objects.all().values('item_id').annotate(counts=Count('id')).filter(date__gte=choose_date[your_date], date__lte=now_time).order_by('-counts')[:50]
#         print(ret.values('id', 'item_id', 'date', 'user_id', 'rating'))
#         # item_name= Commodity.objects.all().values('assin', 'title')
#         # new_ret = chain(item_name)
#
#         # test = chain(item_name, ret)
#         # for item in test:
#         #     print(item)
#
#         # 为每个物品添加对应的title
#         for item in ret:
#             a = Commodity.objects.filter(assin=item['item_id'])
#             try:
#                 item['title'] = a.values('title')[0]['title']
#             except IndexError:
#                 print("don't found: ", item['item_id'])
#
#         ret = dict(data=list(ret))
#         ret = json.dumps(ret, cls=DjangoJSONEncoder)
#         return HttpResponse(ret, content_type='application/json')