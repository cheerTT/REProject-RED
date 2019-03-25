# '''
# @Author: cheertt && xie Liangcai
# @Time:2019年3月11日14:31:35
# @Description: 与小程序端商品相关交互的接口
# 谢良才你这个大胖子
# '''
import json

from django.core import serializers
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
# from django.views.decorators.csrf import csrf_exempt
from api.models import Member, Cart
from django.core.paginator import Paginator
from commodity.models import Commodity, CommodityType
from utils.wechat_utils import WechatUtils
from apps.comment.models import Comment
import django.utils.timezone as timezone
from order.models import Transaction


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
        '''
        商品种类展示
        :param request:
        :return:
        '''
        fields = ['id', 'type_name']
        filters = dict()
        ret = dict(data=list(CommodityType.objects.filter(**filters).values(*fields)))
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')


class CommodityListView(View):

    def get(self, request):
        '''
        分页展示商品列表
        :param request:
        :return:
        '''

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
        '''
        显示商品详细信息
        :param request:
        :return:
        '''
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
        '''
        获取商品的所有评论
        :param request:
        :return:
        '''
        ret = {}
        fields = ['id', 'content', 'joined_date', 'state', 'commodity_id', 'member_id']

        commodity_id = request.GET['id']

        comment_list = Comment.objects.filter(commodity_id=commodity_id).values(*fields)

        for comment in comment_list:
            # print(comment)
            member = Member.objects.filter(id=comment['member_id'])
            # print("member:", type(member))
            # print(member.values('pic_name')[0]['pic_name'])
            comment['nickname'] = member.values('nickname')[0]['nickname']
            comment['avatarUrl'] = member.values('avatarUrl')[0]['avatarUrl']

        ret = json.dumps(dict(data=list(comment_list)), cls=DjangoJSONEncoder)
        # print("ret:", ret)
        return HttpResponse(ret, content_type='application/json')


class CommentAddView(View):

    def get(self, request):
        '''
        添加商品评论
        :param request:
        :return:
        '''
        ret = {}

        commodity_id = request.GET['id']

        auth_cookie = WechatUtils.checkMemberLogin(request)
        score = request.GET['score']

        content = request.GET['content']

        member_id = auth_cookie.id
        Comment.objects.create(
            content=content,
            joined_date=datetime.datetime.now(),
            commodity_id=commodity_id,
            member_id=auth_cookie.id
        )

        Transaction.objects.filter(Q(member_id=member_id) & Q(commodity_id=commodity_id)).update(rating=score)
        ret['msg'] = "评论成功"
        return HttpResponse(json.dumps(ret), content_type='application/json')


class CartAddView(View):
    def get(self, request):
        ret = {}
        commodity_id = request.GET['id']
        auth_cookie = WechatUtils.checkMemberLogin(request)
        member_id = auth_cookie.id

        cart_list = Cart.objects.filter(Q(member_id=member_id) & Q(commodity_id=commodity_id))
        if (cart_list):
            ret['msg'] = "已经加入收藏"
        else:
            Cart.objects.create(
                member_id=member_id,
                commodity_id=commodity_id
            )
            ret['msg'] = "加入收藏成功"
        return HttpResponse(json.dumps(ret), content_type='application/json')


class CartListView(View):
    def get(self, request):
        ret = {}
        fields = ['id', 'imUrl', 'title', 'present_price']
        auth_cookie = WechatUtils.checkMemberLogin(request)
        member_id = auth_cookie.id
        cart_list = Cart.objects.filter(member_id=member_id)
        commodity_list = []
        for cart in cart_list:
            commodity = Commodity.objects.filter(id=cart.commodity_id).values(*fields).first()
            commodity_list.append(commodity)
        ret = json.dumps(dict(data=commodity_list), cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')


class CartDeltView(View):
    def post(self, request):
        ret = {}
        commodity_ids = request.POST['goods'].split(',')
        print("goods",request.POST['goods'])
        print("goods",type(commodity_ids))
        auth_cookie = WechatUtils.checkMemberLogin(request)
        member_id = auth_cookie.id
        for commodity_id in commodity_ids:
            print("hfsdfgs",commodity_id)
            Cart.objects.filter(Q(commodity_id=commodity_id) & Q(member_id=member_id)).delete()
        return HttpResponse(ret, content_type='application/json')
