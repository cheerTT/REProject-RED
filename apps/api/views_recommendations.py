# @Time    : 2019/3/12 11:05
# @Author  : 1234
# @Remark  :
import os
import base64
import json
import uuid
import datetime
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from utils.mixin_utils import LoginRequiredMixin
from utils.face_utils import image_array_align_data
from utils.matrix_utils import Matrix
from utils.wechat_utils import WechatUtils
from reporjectred.settings import BASE_DIR, MODELPATH, MAX_DISTINCT, APPID, SECRET
from facenet.align.detect_face import create_mtcnn
from facenet.facenet import get_model_filenames
from scipy import misc
from django.core import serializers
from api.models import Member
from recommendations.models import Users_Recommendations
from commodity.models import Commodity
from django.core.serializers.json import DjangoJSONEncoder
from recommendations.models import Users_AllRecommendations
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error
from django.core.paginator import Paginator

class TopRecommendationsView(View):
    def get(self, request):
        user = WechatUtils.checkMemberLogin(request)
        user_id = user.id
        recommendations = Users_Recommendations.objects.filter(user_id=user_id)
        commodityidlist = []

        for i in recommendations:
            commodityidlist.append([i.product_id_1, i.product_id_2, i.product_id_3, i.product_id_4, i.product_id_5])

        commoditylist = []
        for assin in commodityidlist[0]:
            commodity = Commodity.objects.filter(assin=assin).values()
            commoditylist.append(list(commodity))

        ret = dict(data = commoditylist)
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')

class AllRecommendationsView(View):
    def get(self, request):
        p = int(request.GET['p'])
        user = WechatUtils.checkMemberLogin(request)
        user_id = user.id
        recommendations = Users_AllRecommendations.objects.filter(user_id=user_id)
        '''
        ※※※这里有个关键问题，由于后端算法和数据库的链接原因，这边得到的Commodityidlist实际上是String类型(只是看起来像list)，不能直接转
        成List使用，所以需要使用split方法把它切分成list。
        '''
        commodityidlist = recommendations[0].products_id
        commodityidlist = commodityidlist.split(',')

        commoditylist = []

        # for assin in commodityidlist:
        #     commodity = Commodity.objects.filter(assin=assin.lstrip()).values()
        #     '''
        #     这里用strip去除一下头部的空格符号。
        #     '''
        #
        #     commoditylist.append(list(commodity))
        #
        page_size = 10 #每页显示的商品数量
        '''
        前端会返回一个值，p：当前页数，以下代码判断该次Get行为是否会超出列表长度。
        每次只查找page_size个值，性能优秀Perfect。
        '''
        have_been_showed_commodityid = p * page_size
        if (have_been_showed_commodityid + page_size > len(commodityidlist)):
            has_more = False
            for i in range(have_been_showed_commodityid, len(commodityidlist) - have_been_showed_commodityid):

                assin = commodityidlist[i]
                commodity = Commodity.objects.filter(assin=assin.lstrip()).values()
                commoditylist.append(list(commodity))
        else :
            has_more = True
            for i in range(have_been_showed_commodityid, have_been_showed_commodityid + page_size):
                assin = commodityidlist[i]
                commodity = Commodity.objects.filter(assin=assin.lstrip()).values()
                commoditylist.append(list(commodity))

        ret = dict(data=commoditylist)
        ret["has_more"] = has_more
        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')
        #
        # paginator = Paginator(commoditylist, page_size)
        # commodity_pages = paginator.page(p)  # 第p页的内容
        #
        # ret = dict(data = list(commodity_pages))
        # ret["has_more"] = commodity_pages.has_next()
        # ret = json.dumps(ret, cls=DjangoJSONEncoder)
        # return HttpResponse(ret, content_type='application/json')

