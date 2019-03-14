from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from api import views_member
from api import views_recommendations
urlpatterns = [
    # 会员信息增改删查操作
    url(r'^member/$', views_member.MemberView.as_view(), name="member"),
    # url(r'^member/savepic', views_member.MemberUploadFace.as_view(), name="member-save-face"),
    url(r'^member/login', csrf_exempt(views_member.MemberLoginView.as_view()), name="member-login"),
    url(r'^member/checkreg', csrf_exempt(views_member.MemberCheckRegView.as_view()), name="member-checkreg"),
    url(r'^recommendations/toprecommendations', csrf_exempt(views_recommendations.TopRecommendationsView.as_view()), name="TopRecommendations"),
    url(r'^recommendations/allrecommendations', csrf_exempt(views_recommendations.AllRecommendationsView.as_view()),
        name="AllRecommendations"),
    # url(r'^user/list$', views.UserListView.as_view(), name="user-list"),
    # url(r'^user/create$', views.UserCreateView.as_view(), name="user-create"),
    # url(r'^user/enable$', views.UserEnableView.as_view(), name="user-enable"),
    # url(r'^user/disable$', views.UserDisableView.as_view(), name="user-disable"),
    # url(r'^user/delete$', views.UserDeleteView.as_view(), name="user-delete"),
    # url(r'^user/detail$', views_user.UserDetailView.as_view(), name="user-detail"),
    # url(r'^user/update$', views_user.UserUpdataView.as_view(), name="user-update"),
    # url(r'^user/create$', views_user.UserCreateView.as_view(), name="user-create"),
    # url(r'^user/delete$', views_user.UserDeleteView.as_view(), name="user-delete"),
    # url(r'^user/enable$', views_user.UserEnableView.as_view(), name="user-enable"),
    # url(r'^user/disable$', views_user.UserDisableView.as_view(), name="user-disable"),
    # url(r'^user/adminpasswdchange$', views_user.AdminPasswdChangeView.as_view(), name="user-adminpasswdchange"),

]