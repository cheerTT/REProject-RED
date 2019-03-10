# @Time    : ${3/10/2019} ${TIME}
# @Author  : $Sutrue
# @Remark  :
from django.conf.urls import url
from hotcommend import views

urlpatterns = [

    url(r'hotcommend/$', views.CommendView.as_view(), name='hotcommend'),
    url(r'^hotcommend/item_rank$', views.ItemRank.as_view(), name='item_rank'),
    url(r'^hotcommend/add_commendation$', views.AddCommendation.as_view(), name='add_commendation'),
    url(r'^hotcommend/hot_list$', views.HotAdd.as_view(), name='hot_add'),
    url(r'hotcommend/to_hot_list', views.ToTheList.as_view(), name='to_hot_list'),
    url(r'^hotcommend/hot_delete', views.HotDeleteView.as_view(), name='hot_delete'),
    # url(r'^hotcommend/item_rank/$', views.SalesQuery.as_view(), name='sales_query'),
]