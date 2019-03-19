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
from order.models import Transaction

class TopRecommendationsView(View):
    def get(self, request):
        user = WechatUtils.checkMemberLogin(request)
        user_id = user.id
        recommendations = Users_Recommendations.objects.filter(user_id=user_id)
        commodityidlist = []

        for i in recommendations:
            commodityidlist.append([i.product_id_1, i.product_id_2, i.product_id_3, i.product_id_4, i.product_id_5])

        commoditylist = []
        for item_id in commodityidlist[0]:
            commodity = Commodity.objects.filter(id=item_id).values().first()
            commoditylist.append(commodity)

        ret = dict(data = commoditylist)

        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        return HttpResponse(ret, content_type='application/json')

class Get_Common_Recommenadations(View):
    def get(self, request):
        user = WechatUtils.checkMemberLogin(request)
        user_id = user.id
        boughtitems = Transaction.objects.filter(member_id=user_id)
        boughtitemkindlist = []

        boughtitemdict = {
            'Baby': 0,
            'Beauty': 0,
            'Grocery_and_Gourmet_Food': 0,
            'Electronics': 0,
            'Office_Products': 0,
            'Pet_Supplies': 0,
            'Sports_and_Outdoors': 0,
            'Home_and_Kitchen': 0,
        }
        commoditylist = []
        sum_of_boughtitem = len(boughtitems)
        for boughtitem in boughtitems:
            boughtitemkindlist.append(boughtitem.commodity.categories.type_name)
            boughtitemdict[boughtitem.commodity.categories.type_name] += 1
            '''
            该用户若是购买了两件以上或者25%以上某种类商品，则给他推送该种类下随机五件商品，注意，Order_by方法损耗较大
            但还是最优随机选择方法。
            '''
        for type in boughtitemdict:
            if (boughtitemdict[type] >= 2 or boughtitemdict[type]/sum_of_boughtitem >=0.25 ):
                recommendations = Commodity.objects.filter(categories__type_name= type).order_by('?')[:5].values()
                commoditylist += recommendations
        ret = dict(data=commoditylist)
        print(ret)
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

        page_size = 10 #每页显示的商品数量
        '''
        前端会返回一个值，p：当前页数，以下代码判断该次Get行为是否会超出列表长度。
        每次只查找page_size个值，性能优秀Perfect。
        '''
        have_been_showed_commodityid = p * page_size
        if (have_been_showed_commodityid + page_size > len(commodityidlist)):
            has_more = False
            for i in range(have_been_showed_commodityid, len(commodityidlist) - have_been_showed_commodityid):

                item_id = commodityidlist[i]
                commodity = Commodity.objects.filter(id=item_id.lstrip()).values().first()
                commoditylist.append(commodity)
        else :
            has_more = True
            for i in range(have_been_showed_commodityid, have_been_showed_commodityid + page_size):
                item_id = commodityidlist[i]
                commodity = Commodity.objects.filter(id=item_id.lstrip()).values().first()
                commoditylist.append(commodity)

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

