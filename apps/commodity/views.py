from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from commodity.models import Commodity, CommodityType, Commodity_price
from commodity.forms import CommodityCreateForm, CommodityUpdateForm, ImageUploadForm
from utils.mixin_utils import LoginRequiredMixin
import json
import re


class CommodityView(LoginRequiredMixin, View):
    def get(self, request):
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

    def get(self, request):
        fields = ['id', 'assin', 'title', 'brand', 'status', 'buyDate', 'present_price', 'categories__type_name']
        filters = dict()
        if 'assin' in request.GET and request.GET['assin']:
            filters['assin__icontains'] = request.GET['assin']
        if 'title' in request.GET and request.GET['title']:
            filters['title__icontains'] = request.GET['title']
        if 'categories' in request.GET and request.GET['categories']:
            filters['categories'] = request.GET['categories']
        # if 'brand' in request.GET and request.GET['brand']:
        #     filters['brand__icontains'] = request.GET['brand']
        if 'status' in request.GET and request.GET['status']:
            filters['status'] = request.GET['status']
        ret = dict(data=list(Commodity.objects.filter(**filters).values(*fields)))

        ret = json.dumps(ret, cls=DjangoJSONEncoder)
        # for data in ret:
        #     print(data['title'])

        return HttpResponse(ret, content_type='application/json')


class CommodityCreateView(LoginRequiredMixin, View):

    def get(self, request):
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
        commodity_create_form = CommodityCreateForm(request.POST)
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

    def get(self, request):
        ret = dict()
        status_list = []
        if 'id' in request.GET and request.GET['id']:
            commodity = get_object_or_404(Commodity, pk=request.GET['id'])
            ret['commodity'] = commodity
        for status in Commodity.commodity_status:
            status_dict = dict(item=status[0], value=status[1])
            status_list.append(status_dict)
        commodity_type = CommodityType.objects.values()
        # role = get_object_or_404(Role, title="销售")
        # user_info = role.userprofile_set.all()
        ret['commodity_type'] = commodity_type
        # ret['user_info'] = user_info
        ret['status_list'] = status_list
        return render(request, 'commodity/commodity_update.html', ret)

    def post(self, request):
        res = dict()
        commodity = get_object_or_404(Commodity, pk=request.POST['id'])
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

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            Commodity.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class CommodityDetailView(LoginRequiredMixin, View):
    """
    商品详情页面
    """

    def get(self, request):
        ret = dict()
        print ("测试")
        print(request.GET.get('assin'))
        print(request.GET)
        if 'assin' in request.GET and request.GET['assin']:
            # commodity = get_object_or_404(Commodity)
            # asset_log = asset.assetlog_set.all()
            commodity = Commodity.objects.filter(assin=request.GET['assin'])
            print(commodity)
            # asset_file = asset.assetfile_set.all()
            ret['commodity'] = commodity[0]
            # ret['asset_log'] = asset_log
            # ret['asset_file'] = asset_file
        return render(request, 'commodity/commodity_detail.html', ret)


class UploadImageView(LoginRequiredMixin, View):
    """
    上传商品图片
    """

    def post(self, request):
        ret = dict(result=False)
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_form.save()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')
