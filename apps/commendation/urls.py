from django.conf.urls import url
from commendation import views

urlpatterns = [

    url(r'^commendation/$', views.CommendView.as_view(), name='commendation'),
    url(r'^commendation/list$', views.CommendListView.as_view(), name='commendation_list'),
    url(r'^sales_query/$', views.SalesQuery.as_view(), name='sales_query'),
]