# @Time    : ${3/10/2019} ${TIME}
# @Author  : $Sutrue
# @Remark  : 视图函数
import json
from datetime import datetime, timedelta
from django.shortcuts import render

from django.shortcuts import HttpResponse
from django.views.generic.base import View
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Count, Sum, F
from django.utils.safestring import mark_safe
from utils.mixin_utils import LoginRequiredMixin

from commodity.models import Commodity
from order.models import Transaction
from hotcommend.models import hot_list, transaction_record


class CommendView(LoginRequiredMixin, View):
    """
    转入热门推荐页
    """
    def get(self, request):
        """
        向前台发送增速最快的商品的信息
        :param request:
        :return:
        """
        # now_time = datetime.now().strftime('%Y-%m-%d')
        # day_7_ago = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d')
        # day_14_ago = (datetime.now() + timedelta(days=-14)).strftime('%Y-%m-%d')
        # day_30_ago = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')
        ret = dict()

        #最近一周的销量
        recent7 = transaction_record.objects.all().values('assin').\
            annotate(sales_count=Count('id')).\
            filter(date__gte='2013-02-26', date__lte='2013-03-11').order_by('date')
        recent14 = transaction_record.objects.all().values('assin').\
            annotate(sales_count=Count('id')).\
            filter(date__gte='2013-02-11', date__lte='2013-03-11').order_by('date')

        inc = {}
        for i in recent7:
            for j in recent14:
                if j['assin'] == i['assin']:
                    try:
                        inc[i['assin']] = i['sales_count'] / (j['sales_count'] - i['sales_count'])
                    except ZeroDivisionError:
                        pass
                    break

        sort_inc = sorted(inc, key=lambda x: inc[x], reverse=True)[:6]


        data = []
        # 根据日期进行循环
        begin = datetime.strptime("2013-02-11", "%Y-%m-%d")
        end = datetime.strptime("2013-03-12", "%Y-%m-%d")
        delta = timedelta(days=1)

        for assin in sort_inc:
            data_sales = list(transaction_record.objects.all().filter(assin=assin).values('date').
                              annotate(sales_count=Count('id')).
                              filter(date__gte='2013-02-11', date__lte='2013-03-11'))
            has_date = []
            #去除日期的时分秒
            for i in data_sales:
                short = i['date'][:10]
                has_date.append(short)
                i['date'] = short

            #将没有销量的日期销量数定位0
            tmp_d = begin
            while tmp_d <= end:
                str_da = str(tmp_d.strftime("%Y-%m-%d"))
                if str_da not in has_date:
                    data_sales.append({'date': str_da, 'sales_count':0})
                tmp_d += delta


            data_sales = sorted(data_sales, key=lambda x: x['date'])
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
        # day_3_ago = (datetime.now() + timedelta(days=-3)).strftime('%Y-%m-%d')
        # day_7_ago = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d')
        day_30_ago = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')

        # choose_date = {'3': day_3_ago, '7': day_7_ago, '30': day_30_ago}

        #接收根据assin查询传来的assin值
        if 'assin' in request.GET and request.GET['assin']:
            ret = Commodity.objects.filter(assin=request.GET['assin']).\
                annotate(commodity=F('id'), commodity__title=F('title')).\
                values('commodity', 'commodity__title', 'status')


            status = '0'
            try:
                status = ret.values('status')[0]['status']
            except IndexError:
                pass

            #判断商品是否下架
            if status == '1':
                sales_count = Transaction.objects.all().\
                    filter(commodity__assin=request.GET['assin']).\
                    values('commodity__assin').annotate(sales_count=Sum('num')).\
                    filter(joined_date__gte=day_30_ago, joined_date__lte=now_time)
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

        ret = Transaction.objects.all().values('commodity', 'commodity__title').\
        annotate(sales_count=Sum('num')).\
        filter(joined_date__gte=day_30_ago, joined_date__lte=now_time).\
        order_by('-sales_count')[:50]

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
        """
        转入排名页
        :param request:
        :return:
        """
        return render(request, 'hotcommend/item_rank.html')


class HotAdd(LoginRequiredMixin, View):
    """
    显示热门推荐列表
    """
    def get(self, request):
        """
        从后端获得hot_list表的商品
        :param request:
        :return:
        """
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


        #将昨天销量前10的自动加入hot_list表中
        now_time = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
        yesterday_count = Transaction.objects.all().values('commodity', 'commodity__assin').\
        annotate(counts=Sum('num')).filter(joined_date__gte=yesterday, joined_date__lte=now_time)[:10]
        for item in yesterday_count:
            if hot_list.objects.filter(assin=item['commodity__assin']).count() == 0:
                temp_b = Commodity.objects.filter(assin=item['commodity__assin']).\
                    values('id', 'assin', 'title', 'categories', 'present_price', 'imUrl')

                hot_commodity = hot_list(assin=temp_b.values('assin')[0]['assin'],
                                         title=temp_b.values('title')[0]['title'],
                                         categories=temp_b.values('categories')[0]['categories'],
                                         imUrl=temp_b.values('imUrl')[0]['imUrl'],
                                         present_price=temp_b.values('present_price')[0]['present_price'],
                                         sales_count=item['counts'], id=temp_b.values('id')[0]['id'])
                hot_commodity.save()

        ret = dict(data=list(hot_list.objects.filter(**filters).values(*fields)))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)

        return HttpResponse(ret, content_type='application/json')


class ToTheList(LoginRequiredMixin, View):
    """
    将选择的商品加入热门商品数据库
    """
    def post(self, request):
        """
        接收前端选择的商品的commodity
        :param request:
        :return:
        """
        ret = dict()
        now_time = datetime.now().strftime('%Y-%m-%d')
        day_30_ago = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')
        fields = ['id', 'assin', 'title', 'categories', 'present_price', 'imUrl', 'status']

        #销量单独获取
        sales_count = Transaction.objects.all().filter(commodity=request.POST['commodity']).\
            values('commodity').annotate(sales_count=Sum('num')).\
            filter(joined_date__gte=day_30_ago, joined_date__lte=now_time)
        count = 0
        try:
            for item in sales_count:
                count += item['sales_count']
        except IndexError:
            count = 0


        temp_a = Commodity.objects.filter(id=request.POST['commodity']).values(*fields)
        #如果hot表中已经存在该商品，则不再放入
        if temp_a.values('status')[0]['status'] == '1':
            if hot_list.objects.filter(assin=temp_a.values('assin')[0]['assin']).count() == 0:
                hot_commodity = hot_list(assin=temp_a.values('assin')[0]['assin'],
                                         title=temp_a.values('title')[0]['title'],
                                         categories=temp_a.values('categories')[0]['categories'],
                                         imUrl=temp_a.values('imUrl')[0]['imUrl'],
                                         present_price=temp_a.values('present_price')[0]['present_price'],
                                         sales_count=count, id=temp_a.values('id')[0]['id'])
                hot_commodity.save()
        return HttpResponse(ret, content_type='application/json')


class HotDeleteView(LoginRequiredMixin, View):
    """
    热门推荐商品删除视图
    """
    def post(self, request):
        """
        接收前端传来的所删除商品的assin
        :param request:
        :return:
        """
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            delete_item = request.POST.get('id').split(',')
            hot_list.objects.filter(id__in=delete_item).delete()

        ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')
