# @Author  : cheertt
# @Time    : 2019/3/3 9:44
# @Remark  : 超级管理员以及商家管理模块
import json
import re
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForm, UserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
User = get_user_model()


class UserBackend(ModelBackend):
    """
    自定义用户验证: setting中对应配置
    AUTHENTICATION_BACKENDS = (
        'users.views.UserBackend',
        )
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(LoginRequiredMixin, View):
    """
    跳转首页视图，其中LoginRequiredMixin用于判断当前用户是否处于登陆状态
    """
    def get(self, request):
        return HttpResponseRedirect('/personal/')


class LoginView(View):
    """
    用户登录认证，通过form表单进行输入合规验证
    django使用会话和中间件来拦截认证系统中的请求对象。他们在每一个请求上都提供一个request.user属性，
    表示当前用户。如果当前用户没有接入，该属性将设置成AnonymousUser的一个实例，否则将会是User实例；
    """
    def get(self, request):
        """
        若用户没有被授权，则跳转到登陆页面，否则显示登陆成功主界面
        :param request:
        :return:
        """
        if not request.user.is_authenticated():
            return render(request, 'users/login.html')
        else:
            return HttpResponseRedirect('/personal/')

    def post(self, request):
        """
        若用户状态为0，在登陆页面显示为未激活；
        若输入用户名与密码与数据库不一致，在登陆界面显示用户名或密码错误；
        若用户没有输入用户名或者密码，在登陆页面显示用户名或密码错误；
        否则，用户登陆成功，保存用户信息至session，并显示跳转之后的主界面；
        :param request:
        :return:
        """
        redirect_to = request.GET.get('next', '/personal/')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 认证用户，如果通过认证后端检查，则返回一个user对象
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    # 用来从视图中登陆一个用户，同时将用户id保存在session中
                    # 使用前必须使用authenticate成功认证这个用户
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    msg = "用户未激活！"
                    ret = {"msg": msg, "login_form": login_form}
                    return render(request, "users/login.html", ret)
            else:
                msg = "用户名或密码错误！"
                ret = {"msg": msg, "login_form": login_form}
                return render(request, "users/login.html", ret)
        else:
            msg = "用户名和密码不能够为空！"
            ret = {"msg": msg, "login_form": login_form}
            return render(request, "users/login.html", ret)


class LogoutView(View):
    """
    用户登出,直接调用django内部方法
    """
    def get(self, request):
        # 登出用户
        logout(request)
        # 根据url名称进行反向解析
        return HttpResponseRedirect(reverse("login"))


class UserView(LoginRequiredMixin, View):
    """
    用户管理，跳转到管理员信息列表
    """
    def get(self, request):
        return render(request, 'users/user-list.html')


class UserListView(LoginRequiredMixin, View):
    """
    获取用户列表信息
    包括，编号、名称、手机、邮件、路径、以及当前用户的状态
    """
    def get(self, request):
        fields = ['id', 'name', 'mobile', 'email', 'url', 'is_active']
        filters = dict()
        if 'select' in request.GET and request.GET.get('select'):
            filters['is_active'] = request.GET.get('select').exclude(username='cheertt')
        ret = dict(data=list(User.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder), content_type='application/json')


class UserCreateView(LoginRequiredMixin, View):
    """
    添加用户，管理员添加商户信息
    """
    def get(self, request):
        users = User.objects.exclude(username='admin')

        ret = {
            'users': users,
        }
        return render(request, 'users/user_create.html', ret)

    def post(self, request):
        user_create_form = UserCreateForm(request.POST)
        if user_create_form.is_valid():
            new_user = user_create_form.save(commit=False)
            new_user.password = make_password(user_create_form.cleaned_data['password'])
            new_user.save()
            user_create_form.save_m2m()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_create_form.errors)
            user_create_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'user_create_form_errors': user_create_form_errors[0]
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserEnableView(LoginRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """
    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=False).update(is_active=True)
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDisableView(LoginRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """
    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=True).update(is_active=False)
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """
    def post(self, request):
        id_nums = request.POST.get('id')
        User.objects.extra(where=["id IN (" + id_nums + ")"]).delete()
        ret = {
            'result': 'true',
            'message': '数据删除成功！'
        }
        return HttpResponse(json.dumps(ret), content_type='application/json')


