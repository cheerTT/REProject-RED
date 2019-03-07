'''
@Author:ttwen
@Time:2019年3月7日10:45:35
@Description: 会员管理的views层
'''

from django.shortcuts import render, get_object_or_404
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from member.models import ApiMember
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import json


class MemberView(LoginRequiredMixin, View):
    '''
    会员查询
    '''
    def get(self, request):
        ret = dict()

        type_list = []
        for type in ApiMember.ApiMember_type:
            type_dict = dict(item=type[0], value=type[1])
            type_list.append(type_dict)
        ret['type_list'] = type_list

        state_list = []
        for state in ApiMember.ApiMember_State:
            state_dict = dict(item=state[0], value=state[1])
            state_list.append(state_dict)
        ret['state_list'] = state_list

        gender_list = []
        for gender in ApiMember.ApiMember_gender:
            gender_dict = dict(item=gender[0], value=gender[1])
            gender_list.append(gender_dict)
        ret['gender_list'] = gender_list

        return render(request, "member/member_list.html", ret)


class MemberListView(LoginRequiredMixin, View):
    '''
    会员列表页面处理方法
    '''
    def get(self, request):
        fields = ['id', 'nickname', 'gender', 'province', 'city', 'type', 'state', 'last_login_date', 'joined_date2']
        filters = dict()
        # print("test:",request.GET['nickname'])
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

        ret = dict(data=list(ApiMember.objects.filter(**filters).values(*fields)))

        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')


class MemberUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        return None

    def post(self, request):
        return None

class MemberDetailView(LoginRequiredMixin, View):
    '''
    用户详情页面
    '''
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            member = get_object_or_404(ApiMember, pk=request.GET.get('id'))
            ret['member'] = member
        return render(request, 'member/member_detail.html', ret)

class MemberEnableView(LoginRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """
    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = ApiMember.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(state='1').update(state='0')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class MemberDisableView(LoginRequiredMixin, View):
    """
    锁定用户：单个或批量锁定
    """
    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = ApiMember.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(state='0').update(state='1')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')
