# @Time    : 2019/3/6 20:00
# @Author  : Virus
# @Remark  :


from django.conf.urls import url

from recommendations import views

urlpatterns = [
    url(r'recommendations/$', views.RecommendationsView.as_view(), name="recommendations"),
    url(r'^recommendations/list$', views.RecommendationsListView.as_view(), name="recommendations-list"),
    url(r'^recommendations/detail$', views.RecommendationsDetailView.as_view(), name="detail"),]
    # url(r'^user/detail$', views_user.UserDetailView.as_view(), name="user-detail"),
    # url(r'^user/update$', views_user.UserUpdataView.as_view(), name="user-update"),
    # url(r'^user/create$', views_user.UserCreateView.as_view(), name="user-create"),
    # url(r'^user/delete$', views_user.UserDeleteView.as_view(), name="user-delete"),
    # url(r'^user/enable$', views_user.UserEnableView.as_view(), name="user-enable"),
    # url(r'^user/disable$', views_user.UserDisableView.as_view(), name="user-disable"),
    # url(r'^user/adminpasswdchange$', views_user.AdminPasswdChangeView.as_view(), name="user-adminpasswdchange"),
