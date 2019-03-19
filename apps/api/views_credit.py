#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Time    : 2019/3/18 19:25
# @Author  : TTWen
# @Remark  : 会员积分相关操作

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

class CreditCreateView(View):
    def get(self, request):
        ret = []
        return HttpResponse(json.dumps(ret), content_type='application/json')

class CreditListView(View):
    def get(self, request):
        ret = []
        return HttpResponse(json.dumps(ret), content_type='application/json')