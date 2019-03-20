# '''
# @Author: cheertt && xie Liangcai
# @Time:2019年3月11日14:31:35
# @Description: 与小程序端商品相关交互的接口
# '''
import json
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
# from django.views.decorators.csrf import csrf_exempt
from api.models import Member
from django.core.paginator import Paginator
from commodity.models import Commodity, CommodityType
from utils.wechat_utils import WechatUtils
from apps.comment.models import Comment


class CommoditySearchView(View):

    def get(self, request):
        # print("111111111111111111111111111111")
        print(request.GET['s'])
        s = request.GET['s']
        fields = ['id', 'assin', 'title', 'imUrl', 'present_price']

        comms = Commodity.objects.filter(assin__contains=s).values(*fields)
        ret = dict(data=list(comms))
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')

    def post(self, request):
        pass


class CommodityTypeView(View):

    def get(self, request):
        fields = ['id', 'type_name']
        filters = dict()
        ret = dict(data=list(CommodityType.objects.filter(**filters).values(*fields)))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')


class CommodityListView(View):

    def get(self, request):

        fields = ['id', 'assin', 'title', 'brand', 'status', 'buyDate', 'present_price', 'categories__type_name',
                  'imUrl']
        filters = dict()
        if 'commodity_id' in request.GET and request.GET['commodity_id']:
            filters['categories'] = request.GET['commodity_id']
        if 'mix_kw' in request.GET and request.GET['mix_kw']:
            filters['title__icontains'] = request.GET['mix_kw']

        p = int(request.GET['p'])

        page_size = 10
        commodity_list = Commodity.objects.filter(**filters).values(*fields).order_by("id")
        paginator = Paginator(commodity_list, page_size)

        commodity_pages = paginator.page(p)  # 第p页的内容
        # print("是否有下一页：",commodity_pages.has_next())
        ret = dict(data=list(commodity_pages))
        ret["has_more"] = commodity_pages.has_next()
        ret = json.dumps(ret, cls=DjangoJSONEncoder)

        return HttpResponse(ret, content_type='application/json')


class CommodityInfoView(View):
    def get(self, request):
        fields = ['id', 'assin', 'title', 'brand', 'status', 'buyDate', 'present_price', 'categories__type_name',
                  'imUrl', 'description']
        filters = dict()
        if 'id' in request.GET and request.GET['id']:
            filters['id'] = request.GET['id']
        commodity_info = Commodity.objects.filter(**filters).values(*fields)
        ret = dict(data=list(commodity_info))
        # ret["code"]=200
        # ret["msg"]="操作成功~"
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        # print("ret:", ret)
        return HttpResponse(ret, content_type='application/json')


class CommodityCommentsView(View):
    def get(self, request):
        ret = {}
        fields = ['id', 'content', 'joined_date', 'state', 'commodity_id', 'member_id']
        # fields = ['id', 'pic_name', 'avatarUrl']
        # if 'id' in request.GET and request.GET['id']:
        #     filters['id'] = request.GET['id']
        #     print("id:",filters['id'])
        commodity_id = request.GET['id']
        # ua = request.META.get("HTTP_AUTHORIZATION")
        # auth_cookie = WechatUtils.checkMemberLogin(request)

        # ret['id'] = auth_cookie.id
        print("commodity_id", commodity_id)
        comment_list = Comment.objects.filter(commodity_id=commodity_id).values(*fields)

        print("type:", type(comment_list[0]))
        for comment in comment_list:
            print(comment)
            member = Member.objects.filter(id=comment['member_id'])
            # print("member:", type(member))
            print(member.values('pic_name')[0]['pic_name'])
            comment['nickname'] = member.values('nickname')[0]['nickname']
            comment['avatarUrl'] = member.values('avatarUrl')[0]['avatarUrl']

        ret = json.dumps(dict(data=list(comment_list)), cls=DjangoJSONEncoder)
        # print("ret:", ret)
        return HttpResponse(ret, content_type='application/json')


class CommentAddView(View):
    def get(self,request):
        pass