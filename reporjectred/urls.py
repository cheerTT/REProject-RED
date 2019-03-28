"""reporjectred URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from reporjectred.settings import MEDIA_ROOT
from users.views import IndexView, LoginView, LogoutView
from personal.views import PersonalView, UserInfoView, UploadImageView, \
    PasswdChangeView
from api.views_member import FaceView


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^$', IndexView.as_view(), name='index'),
    # 用户登录
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),

    url(r'^personal/$', PersonalView.as_view(), name="personal"),
    url(r'^personal/userinfo', UserInfoView.as_view(), name="personal-user_info"),
    url(r'^personal/uploadimage', UploadImageView.as_view(), name="personal-uploadimage"),
    url(r'^personal/passwordchange', PasswdChangeView.as_view(), name="personal-passwordchange"),

    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^commodity/', include('commodity.urls', namespace='commodity')),

    url(r'^recommendations/', include('recommendations.urls', namespace='recommendations')),
    url(r'^comment/', include('apps.comment.urls', namespace='comment')),

    url(r'^hotcommend/', include('hotcommend.urls', namespace='hotcommend')),

    url(r'^api/face/$', FaceView.as_view(), name="face"),

    url(r'^api/', include('api.urls', namespace='api')),
]
