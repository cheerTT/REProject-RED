'''
@Author:ttwen
@Time:2019年3月7日10:45:35
@Description: 会员管理的urls层
'''

from django.conf.urls import url

from member import views

urlpatterns = [

    url(r'member/$', views.MemberView.as_view(), name='member'),

    url(r'^member/list$', views.MemberListView.as_view(), name="member-list"),

    # 小程序调用，web端没有需求
    url(r'^member/update$', views.MemberUpdateView.as_view(), name="member-update"),

    url(r'^member/enable$', views.MemberEnableView.as_view(), name="member-enable"),

    url(r'^member/disable$', views.MemberDisableView.as_view(), name="member-disable"),

    url(r'^member/detail$', views.MemberDetailView.as_view(), name="member-detail"),
]

