#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Time    : 2019/3/18 19:25
# @Author  : TTWen
# @Remark  : 会员积分相关操作

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

from api.models import Credit


class CreditListView(View):
    def get(self, request):

        ret = []
        print("coming")

        fields = ['id', 'behave', 'creditpoints', 'credittype', 'createtime', 'userid']
        filters = dict()
        if 'userid' in request.GET and request.GET['userid']:
            filters['userid'] = request.GET['userid']
        credit_list = Credit.objects.filter(**filters).values(*fields)
        ret = dict(data=list(credit_list))
        # print("ret:",ret)
        return HttpResponse(json.dumps(ret, default=str), content_type='application/json')

class ShareView(View):
    def get(self, request):
        print("share request:",request)
        ret = []
        return HttpResponse(json.dumps(ret), content_type='application/json')