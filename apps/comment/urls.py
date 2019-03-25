from django.conf.urls import url

from comment import views

urlpatterns = [

    url(r'^comment/$', views.CommentView.as_view(), name='comment'),
    url(r'^comment/list', views.CommentListView.as_view(), name='comment-list'),
    url(r'^comment/enable$', views.CommentEnableView.as_view(), name="comment-enable"),
    url(r'^comment/disable$', views.CommentDisableView.as_view(), name="comment-disable"),

]
