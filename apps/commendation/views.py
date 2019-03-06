from django.shortcuts import render
import json

from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponse
from django.contrib.auth import get_user_model
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from commendation.models import Commendation

class CommendView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'commendation/commendation.html')


#通过QuerySet的values方法来获取指定字段列的数据内容，转换QuerySet类型最终序列化成json串，返回数据访问接口
class CommendListView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, 'commendation/commendation_list.html')

class SalesQuery(LoginRequiredMixin, View):
    #查询近几日的销量
    def get(self, request):
        return render(request, 'commendation/sales_query.html')