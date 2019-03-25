#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019/3/18 19:25
# @Author  : TTWen
# @Remark  : 会员积分相关操作
import datetime
import json

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

from api.models import Credit
from utils.wechat_utils import WechatUtils


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
    def post(self, request):
        print("share request:", request.POST['url'])
        ret = {}
        # behave=2
        auth_cookie = WechatUtils.checkMemberLogin(request)
        member_id = auth_cookie.id
        now = datetime.datetime.now()  # 现在的时间
        last_behave = Credit.objects.filter(Q(userid_id=member_id) & Q(behave=2))
        if (last_behave):
            last_share_date = last_behave.last().createtime  # 上次分享的时间

            if (now.strftime('%Y-%m-%d') != last_share_date.strftime('%Y-%m-%d')):
                print("今天第一次分享")
                ret['first_time_share'] = '恭喜你，今天首次分享获得3积分'
                print("credit insert:")
                Credit.objects.create(
                    behave=2,
                    creditpoints=3,
                    credittype=0,
                    createtime=datetime.datetime.now(),
                    userid_id=member_id
                )

        else:
            Credit.objects.create(
                behave=2,
                creditpoints=3,
                credittype=0,
                createtime=datetime.datetime.now(),
                userid_id=member_id
            )
        return HttpResponse(json.dumps(ret), content_type='application/json')
