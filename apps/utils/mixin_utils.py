"""
登陆验证，相当于一个过滤器
"""
# @Author  : cheertt
# @Time    : 2019/3/2 20:22
# @Remark  : 判断用户是否登陆
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """
    # 用户登陆系统才可以访问某些页面
    # 如果用户没有登陆而直接访问就会跳转到登陆界面
    # 用户在跳转的登陆页面完成登陆后，自动访问跳转前的url
    """
    @classmethod
    def as_view(cls, **init_kwargs):
        """
        判断用户是否登陆
        :param init_kwargs:
        :return:
        """
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return login_required(view)
