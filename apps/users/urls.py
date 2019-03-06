from django.conf.urls import url

from users import views

urlpatterns = [
    # 用户增改删查操作
    url(r'^user/$', views.UserView.as_view(), name="user"),
    url(r'^user/list$', views.UserListView.as_view(), name="user-list"),
    url(r'^user/create$', views.UserCreateView.as_view(), name="user-create"),
    url(r'^user/enable$', views.UserEnableView.as_view(), name="user-enable"),
    url(r'^user/disable$', views.UserDisableView.as_view(), name="user-disable"),
    url(r'^user/delete$', views.UserDeleteView.as_view(), name="user-delete"),
    # url(r'^user/detail$', views_user.UserDetailView.as_view(), name="user-detail"),
    # url(r'^user/update$', views_user.UserUpdataView.as_view(), name="user-update"),
    # url(r'^user/create$', views_user.UserCreateView.as_view(), name="user-create"),
    # url(r'^user/delete$', views_user.UserDeleteView.as_view(), name="user-delete"),
    # url(r'^user/enable$', views_user.UserEnableView.as_view(), name="user-enable"),
    # url(r'^user/disable$', views_user.UserDisableView.as_view(), name="user-disable"),
    # url(r'^user/adminpasswdchange$', views_user.AdminPasswdChangeView.as_view(), name="user-adminpasswdchange"),

]