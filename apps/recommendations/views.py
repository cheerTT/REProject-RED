import json
import re
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from utils.mixin_utils import LoginRequiredMixin
#from .forms import LoginForm, UserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.hashers import make_password
from recommendations.models import Users_Recommendations
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from commodity.models import Commodity

class RecommendationsView(LoginRequiredMixin, View):


    def get(self, request):
        # ret = SystemSetup.getSystemSetupLastData()
        return render(request, 'recommendations/recommendations_list.html')

class RecommendationsDetailView(LoginRequiredMixin, View):
    """
    商品详情页面
    """

    def get(self, request):
        ret = dict()
        print(request.GET)
        if 'user_id' in request.GET and request.GET['user_id']:
            print(request.GET['user_id'])
            recommendations = Users_Recommendations.objects.filter(user_id=request.GET['user_id'])
            commodityidlist = []
            for i in recommendations:
                commodityidlist.append([i.product_id_1, i.product_id_2, i.product_id_3,i.product_id_4,i.product_id_5])
            #print(commodityidlist)
            commoditylist = []
            for assin in commodityidlist[0]:
                commodity = Commodity.objects.filter(assin=assin)
                commoditylist.append(commodity[0])
            #print(commoditylist)
            # print("this is ")
            # print(commodity)
            # ret['commodity'] = commodity[0]
            ret['commodity_1'] = commoditylist[0]
            ret['commodity_2'] = commoditylist[1]
            ret['commodity_3'] = commoditylist[2]
            ret['commodity_4'] = commoditylist[3]
            ret['commodity_5'] = commoditylist[4]
        return render(request, 'recommendations/recommendations_details.html', ret)

class RecommendationsListView(LoginRequiredMixin, View):
    """
    获取用户列表信息
    """

    def get(self, request):
        fields = ['user_id', 'product_id_1', 'product_id_2', 'product_id_3', 'product_id_4', 'product_id_5']
        filters = dict()
        print(request.GET.get('user_id'))
        if 'user_id' in request.GET and request.GET['user_id']:
            filters['user_id__icontains'] = request.GET['user_id']
        if 'product_id_1' in request.GET and request.GET['product_id_1']:
            filters['product_id_1__icontains'] = request.GET['product_id_1']
        if 'product_id_2' in request.GET and request.GET['product_id_2']:
            filters['product_id_2__icontains'] = request.GET['product_id_2']
        if 'product_id_3' in request.GET and request.GET['product_id_3']:
            filters['product_id_3__icontains'] = request.GET['product_id_3']
        if 'product_id_4' in request.GET and request.GET['product_id_4']:
            filters['product_id_4__icontains'] = request.GET['product_id_4']
        if 'product_id_5' in request.GET and request.GET['product_id_5']:
            filters['product_id_5__icontains'] = request.GET['product_id_5']
        ret = dict(data=list(Users_Recommendations.objects.filter(**filters).values(*fields)))

        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')