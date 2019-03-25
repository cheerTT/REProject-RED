'''
@Author:ttwen
@Time:2019年3月7日10:45:35
@Description: 会员管理的views层
'''

from django.shortcuts import render, get_object_or_404
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from api.models import Member
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from order.models import Transaction
from utils.toolkit import get_month_member_count, get_member_gender, get_monthly_sale_count
import json



class MemberView(LoginRequiredMixin, View):
    '''会员查询'''

    def get(self, request):
        '''
        get方法
        :param request:页面的请求
        :return:跳转member/member_list.html页面
        '''
        ret = dict()

        type_list = []
        for type in Member.type_choices:
            type_dict = dict(item=type[0], value=type[1])
            type_list.append(type_dict)
        ret['type_list'] = type_list

        state_list = []
        for state in Member.state_choices:
            state_dict = dict(item=state[0], value=state[1])
            state_list.append(state_dict)
        ret['state_list'] = state_list

        gender_list = []
        for gender in Member.gender_choices:
            gender_dict = dict(item=gender[0], value=gender[1])
            gender_list.append(gender_dict)
        ret['gender_list'] = gender_list

        # 月度新增用户数量
        month_member_count = get_month_member_count()
        result1 = month_member_count[0]['count']
        ret['month_member_count'] = result1

        # 用户性别统计
        result2 = get_member_gender()[0]['count']
        ret['member_gender'] = result2

        return render(request, "member/member_list.html", ret)


class MemberListView(LoginRequiredMixin, View):
    '''会员列表页面处理方法'''
    def get(self, request):
        '''
        get方法
        :param request:来自页面的请求
        :return:返回会员信息
        '''
        fields = ['id', 'openid', 'pic_name', 'nickname', 'gender', 'city', 'province', 'state', 'last_login_date', 'faceid', 'joined_date1', 'joined_date2', 'avatarUrl', 'codeVerify', 'type',]
        filters = dict()

        if 'nickname' in request.GET and request.GET['nickname']:
            filters['nickname__icontains'] = request.GET['nickname']
        if 'type' in request.GET and request.GET['type']:
            filters['type'] = request.GET['type']
        if 'state' in request.GET and request.GET['state']:
            filters['state'] = request.GET['state']

        if 'beginDate' in request.GET and request.GET['beginDate']:
            filters['joined_date2__gte'] = request.GET['beginDate']
        if 'endDate' in request.GET and request.GET['endDate']:
            filters['joined_date2__lte'] = request.GET['endDate']

        member_list = Member.objects.filter(**filters).values(*fields)
        for member in member_list:
            if member['openid'] == None:
                member['openid'] = 0
            if member['nickname'] == '':
                member['nickname'] = '暂无'
            if member['gender'] == '暂无':
                member['gender'] = 0
            if member['city'] == '':
                member['city'] = '暂无'
            if member['province'] == '':
                member['province'] = '暂无'
            if member['last_login_date'] == None:
                member['city'] = '2019-01-01'
            if member['joined_date2'] == None:
                member['joined_date2'] = '2019-01-01'
            if member['codeVerify'] == None:
                member['codeVerify'] = '暂无'
        ret = dict(data=list(member_list))
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')

class MemberDetailView(LoginRequiredMixin, View):
    '''用户详情页面'''
    def get(self, request):
        '''
        get方法
        :param request:页面的请求
        :return: 跳转member/member_detail.html页面
        '''
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            member = Member.objects.filter(id=request.GET['id'])
            ret['member'] = member[0]
            member = get_object_or_404(Member, pk=request.GET.get('id'))
            ret['member'] = member

        boughtitems = Transaction.objects.filter(member_id=request.GET['id'])
        boughtitemkindlist = []
        boughtitemdict = {
            'Baby': {'label':"有娃", 'value':0},
            'Beauty': {'label':"爱美", 'value':0},
            'Grocery_and_Gourmet_Food': {'label':"吃货", 'value':0},
            'Electronics': {'label':"电子发烧友", 'value':0},
            'Office_Products': {'label':"办公一族", 'value':0},
            'Pet_Supplies': {'label':"家有宠物", 'value':0},
            'Sports_and_Outdoors': {'label':"运动", 'value':0},
            'Home_and_Kitchen': {'label':"家庭", 'value':0},
        }


        sum_of_boughtitem = len(boughtitems)
        sum_of_price = 0
        rate_of_type = 0
        ave_of_ratings = 0
        predict_age = 20

        for boughtitem in boughtitems:
            boughtitemkindlist.append(boughtitem.commodity.categories.type_name)
            boughtitemdict[boughtitem.commodity.categories.type_name]['value'] += 1
            sum_of_price += boughtitem.commodity.present_price
            ave_of_ratings += boughtitem.rating


        ave_of_ratings = ave_of_ratings / sum_of_boughtitem
        current_max = 0
        for key in boughtitemdict:
            if boughtitemdict[key]['value'] > current_max:
                current_max = boughtitemdict[key]['value']
        rate_of_type = current_max / sum_of_boughtitem



        if boughtitemdict['Baby']['value'] > 0:
            predict_age += 10

        frequent_of_buy = sum_of_boughtitem if sum_of_boughtitem < 25 else 25
        sum_of_price = sum_of_price if sum_of_price < 250 else 250



        ret['sum_of_boughtitem'] = sum_of_boughtitem
        ret['frequent_of_buy'] = frequent_of_buy
        ret['boughtitemdict'] = boughtitemdict
        ret['rate_of_type'] = rate_of_type
        ret['ave_of_ratings'] = ave_of_ratings
        ret['sum_of_price'] = sum_of_price
        ret['predict_age'] = predict_age


        return render(request, 'member/member_detail.html', ret)

class MemberEnableView(LoginRequiredMixin, View):
    """启用用户：单个或批量启用"""
    def post(self, request):
        '''
        post方法
        :param request: 页面的request请求
        :return: 返回启用成功的信息
        '''
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Member.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(state='1').update(state='0')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class MemberDisableView(LoginRequiredMixin, View):
    """锁定用户：单个或批量锁定"""
    def post(self, request):
        '''
        post方法
        :param request:来自页面的请求
        :return: 返回锁定成功的信息
        '''
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Member.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(state='0').update(state='1')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')
