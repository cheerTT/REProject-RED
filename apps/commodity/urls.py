
from django.conf.urls import url

from commodity import views

urlpatterns = [

    url(r'commodity/$', views.CommodityView.as_view(), name='commodity'),
    url(r'^commodity/list$', views.CommodityListView.as_view(), name="commodity-list"),
    url(r'^commodity/create$', views.CommodityCreateView.as_view(), name="create"),
    url(r'^commodity/update$', views.CommodityUpdateView.as_view(), name="update"),
    url(r'^commodity/delete$', views.CommodityDeleteView.as_view(), name='delete'),
    url(r'^commodity/detail$', views.CommodityDetailView.as_view(), name="detail"),
    url(r'^commodity/uploadimage$', views.UploadImageView.as_view(), name="commodity-uploadimage"),
    # url(r'^list', views_commodity.AssetListView.as_view(), name="list"),
    # url(r'^create', views_commodity.AssetCreateView.as_view(), name="create"),
    # url(r'^update', views_commodity.AssetUpdateView.as_view(), name="update"),
    # url(r'^detail', views_commodity.AssetDetailView.as_view(), name="asset-detail"),
    # url(r'^delete', views_commodity.AssetDeleteView.as_view(), name='delete'),
    # url(r'^upload', views_commodity.AssetUploadView.as_view(), name='upload'),
]
