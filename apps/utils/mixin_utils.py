from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# class LoginRequiredMixin(object):
#     @method_decorator(login_required(login_url='/login/'))
#     def dispath(self, request, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

# 用户登陆系统才可以访问某些页面
# 如果用户没有登陆而直接访问就会跳转到登陆界面
# 用户在跳转的登陆页面完成登陆后，自动访问跳转前的url
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return login_required(view)
