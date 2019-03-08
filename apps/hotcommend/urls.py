from django.conf.urls import url
from hotcommend import views

urlpatterns = [

    url(r'hotcommend/$', views.CommendView.as_view(), name='hotcommend'),
    url(r'^hotcommend/item_rank$', views.ItemRank.as_view(), name='item_rank'),
    url(r'^hotcommend/add_commendation$', views.AddCommendation.as_view(), name='add_commendation'),
    # url(r'^hotcommend/item_rank/$', views.SalesQuery.as_view(), name='sales_query'),
]