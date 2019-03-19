# @Author  : cheertt
# @Time    : 2019/3/19 9:44
# @Remark  : 评论管理模块
import json
from django.shortcuts import render
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from apps.comment.models import Comment


# Create your views here.
class CommentView(LoginRequiredMixin, View):
    """
    评论管理，跳转到管理员信息列表
    """
    def get(self, request):
        return render(request, 'comment/comment-list.html')


class CommentListView(LoginRequiredMixin, View):
    """
    获取用户列表信息
    """
    def get(self, request):
        fields = ['id', 'content', 'joined_date', 'member__nickname', 'commodity__title', 'state']
        filters = dict()
        print('1111111111111111111111111111')
        print(type(request.GET.get('select')))
        if 'select' in request.GET and request.GET.get('select'):
            if request.GET.get('select') == 'True':
                filters['state'] = '0'
            elif request.GET.get('select') == 'False':
                filters['state'] = '1'
        ret = dict(data=list(Comment.objects.filter(**filters).values(*fields)))
        print(ret)
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')


class CommentEnableView(LoginRequiredMixin, View):
    """
    启用评论状态：单个或批量启用
    """
    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Comment.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(state='1').update(state='0')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class CommentDisableView(LoginRequiredMixin, View):
    """
    禁用评论状态：单个或批量禁用
    """
    def post(self, request):
        print('禁用')
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Comment.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(state='0').update(state='1')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')

