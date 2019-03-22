# @Time   : 2019/3/10 21:03
# @Author : liyuming
# @Remark : 登录主界面信息展示处理
import json
import re
import calendar
from datetime import date, timedelta
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from utils.mixin_utils import LoginRequiredMixin
from .models import WorkOrder
from .forms import UserUpdateForm, ImageUploadForm
from users.forms import AdminPasswdChangeForm
from utils.toolkit import get_month_member_count, get_member_gender, get_monthly_sale_count

User = get_user_model()


class PersonalView(LoginRequiredMixin, View):
    """
    我的工作台,用于显示个人信息，提高用户体验
    """
    def get(self, request):

        start_date = date.today().replace(day=1)
        _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
        end_date = start_date + timedelta(days=days_in_month)
        ret = dict()
        ret['start_date'] = start_date

        # 工作台最上方本月：新用户数、订单总数、订单金额、新商品数
        ret['new_user_this_month'] = 0
        ret['new_order_this_month'] = 0
        ret['new_profit_this_month'] = 0
        ret['new_commodity_this_month'] = 0

        # 月度新增用户数量
        month_member_count = get_month_member_count(value=int(request.GET.get('value', 0)))
        result1 = month_member_count[0]['count']
        for i in result1:
            ret['new_user_this_month'] += i
        ret['month_member_count'] = result1

        # 用户性别统计
        result2 = get_member_gender(value=int(request.GET.get('value', 0)))[0]['count']
        ret['member_gender'] = result2

        # 本月营业额统计
        result3, order_num, new_commo_num, type_num_result, commo_num_array = get_monthly_sale_count(value=0)
        for i in result3:
            ret['new_profit_this_month'] += i
        ret['monthly_sale_count'] = result3
        ret['new_order_this_month'] = order_num
        ret['new_profit_this_month'] = round(ret['new_profit_this_month'],2)

        # 本月新增商品数统计
        ret['new_commodity_this_month'] = new_commo_num

        # 本月售出商品各种类数量
        ret['type_num_result'] = type_num_result

        # 统计全年12个月份8种类商品的销量
        ret['commo_num_array'] = commo_num_array

        return render(request, 'personal/personal_index.html', ret)


class UserInfoView(LoginRequiredMixin, View):
    """
    个人中心：个人信息查看和修改
    """
    def get(self, request):
        return render(request, 'personal/userinfo/user_info.html')

    def post(self, request):
        ret = dict(status="fail")
        user = User.objects.get(id=request.POST['id'])
        user_update_form = UserUpdateForm(request.POST, instance=user)
        if user_update_form.is_valid():
            user_update_form.save()
            ret = {"status": "success"}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    个人中心：上传头像
    """
    def post(self, request):
        ret = dict(result=False)
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class PasswdChangeView(LoginRequiredMixin, View):
    """
    登陆用户修改个人密码
    """
    def get(self, request):
        ret = dict()
        user = get_object_or_404(User, pk=int(request.user.id))
        ret['user'] = user
        return render(request, 'personal/userinfo/passwd-change.html', ret)

    def post(self, request):

        user = get_object_or_404(User, pk=int(request.user.id))
        form = AdminPasswdChangeForm(request.POST)
        if form.is_valid():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(form.errors)
            admin_passwd_change_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'admin_passwd_change_form_errors': admin_passwd_change_form_errors[0]
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')
