from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from commodity.models import Commodity, CommodityType, Commodity_price
from commodity.forms import CommodityCreateForm, CommodityUpdateForm
from utils.mixin_utils import LoginRequiredMixin
import json
import re
import os
from PIL import Image
from django.views.decorators.csrf import csrf_exempt


class CommodityView(LoginRequiredMixin, View):

    def get(self, request):
        '''
        get方法
        :param request:
        :return:跳转到商品列表页面
        '''
        ret = dict()
        status_list = []
        for status in Commodity.commodity_status:
            status_dict = dict(item=status[0], value=status[1])
            status_list.append(status_dict)
        commodity_types = CommodityType.objects.all()
        ret['status_list'] = status_list
        ret['commodity_types'] = commodity_types
        return render(request, 'commodity/commodity_list.html', ret)


class CommodityListView(LoginRequiredMixin, View):
    """商品显示页面"""

    def get(self, request):
        '''
        get方法
        :param request:
        :return: 返回商品信息列表到前端
        '''
        fields = ['id', 'assin', 'title', 'brand', 'status', 'buyDate', 'present_price', 'categories__type_name']
        filters = dict()
        if 'assin' in request.GET and request.GET['assin']:
            filters['assin__icontains'] = request.GET['assin']
        if 'title' in request.GET and request.GET['title']:
            filters['title__icontains'] = request.GET['title']
        if 'categories' in request.GET and request.GET['categories']:
            filters['categories'] = request.GET['categories']
        if 'status' in request.GET and request.GET['status']:
            filters['status'] = request.GET['status']

        commodity_list = Commodity.objects.filter(**filters).values(*fields)
        for commodity in commodity_list:
            title = commodity['title']
            if len(str(title)) > 50:
                commodity['title'] = '{}...'.format(str(title)[0:50])

        ret = json.dumps(dict(data=list(commodity_list)), cls=DjangoJSONEncoder)

        return HttpResponse(ret, content_type='application/json')


class CommodityCreateView(LoginRequiredMixin, View):
    """添加商品页面"""

    def get(self, request):
        '''

        :param request:
        :return:跳转到添加商品页面
        '''
        ret = dict()
        status_list = []
        for status in Commodity.commodity_status:
            status_dict = dict(item=status[0], value=status[1])
            status_list.append(status_dict)
        commodity_type = CommodityType.objects.all()
        ret['commodity_type'] = commodity_type
        ret['status_list'] = status_list
        return render(request, 'commodity/commodity_create.html', ret)

    def post(self, request):
        res = dict()
        commodity_create_form = CommodityCreateForm(request.POST, request.FILES)
        if commodity_create_form.is_valid():
            commodity_create_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(commodity_create_form.errors)
            commodity_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'commodity_form_errors': commodity_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class CommodityUpdateView(LoginRequiredMixin, View):
    """商品信息修改页面"""

    def get(self, request):
        '''

        :param request:
        :return: 跳转到修改商品信息页面
        '''
        ret = dict()
        status_list = []
        if 'id' in request.GET and request.GET['id']:
            commodity = Commodity.objects.filter(id=request.GET['id'])
            ret['commodity'] = commodity[0]
        for status in Commodity.commodity_status:
            status_dict = dict(item=status[0], value=status[1])
            status_list.append(status_dict)
        commodity_type = CommodityType.objects.values()
        ret['commodity_type'] = commodity_type
        ret['status_list'] = status_list
        return render(request, 'commodity/commodity_update.html', ret)

    def post(self, request):
        res = dict()
        commodity = Commodity.objects.filter(assin=request.GET['assin'])[0]
        commodity_update_form = CommodityUpdateForm(request.POST, instance=commodity)
        if commodity_update_form.is_valid():
            commodity_update_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(commodity_update_form.errors)
            commodity_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'commodity_form_errors': commodity_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class CommodityDeleteView(LoginRequiredMixin, View):
    '''

        :param request:
        :return: 返回商品删除成功信息
    '''

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            Commodity.objects.filter(id__in=id_list).delete()

        ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class CommodityEnableView(LoginRequiredMixin, View):
    '''
       上架商品视图
    '''

    def post(self, request):
        '''
        post方法
        :param request: 页面的request请求
        :return: 返回商品上架成功的信息
        '''
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Commodity.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(status='0').update(status='1')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class CommodityDisableView(LoginRequiredMixin, View):
    '''下架商品视图'''

    def post(self, request):
        '''
        :param request:
        :return: 返回商品下架成功信息
        '''

        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Commodity.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(status='1').update(status='0')
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class CommodityDetailView(LoginRequiredMixin, View):
    """商品详情页面"""

    def get(self, request):
        '''
        :param request:
        :return: 跳转到商品详情页面
        '''
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            commodity = Commodity.objects.filter(id=request.GET['id'])
            ret['commodity'] = commodity[0]
        return render(request, 'commodity/commodity_detail.html', ret)


class UploadImageView(LoginRequiredMixin, View):
    '''
        上传商品图片
    '''

    def get(self, request):
        ret = dict()
        assin = request.GET['assin']
        categories = request.GET['categories']
        ret['assin'] = assin
        ret['categories'] = categories
        print("Image get()")
        return render(request, 'commodity/commodity_upload.html', ret)

    def post(self, request):
        res = dict(status='fail')
        File = request.FILES.get("file_content")
        print(File.name)
        accessory_dir = "media/commImage/" + request.POST['categories']
        if not os.path.isdir(accessory_dir):  # 判断是否有这个目录，没有就创建
            os.mkdir(accessory_dir)
        filename = accessory_dir + "/" + request.POST['assin'] + ".jpg"
        print(filename)
        with open(filename, 'wb+') as f:
            # 分块写入文件
            for chunk in File.chunks():
                f.write(chunk)
        res['status'] = 'success'
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
