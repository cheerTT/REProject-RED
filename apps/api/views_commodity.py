# '''
# @Author: cheertt
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
from commodity.models import Commodity


class CommoditySearchView(View):

    def get(self, request):
        print("111111111111111111111111111111")
        print(request.GET['s'])
        s = request.GET['s']
        fields = ['id', 'assin']

        comms = Commodity.objects.filter(assin__contains=s).values(*fields)
        ret = dict(data=list(comms))
        print(ret)
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')

    def post(self, request):
        pass

