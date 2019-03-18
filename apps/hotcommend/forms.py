# @Time    : ${3/10/2019} ${TIME}
# @Author  : $Sutrue
# @Remark  :

from django import forms
from hotcommend.models import *

class SalesQueryForm(forms.ModelForm):
    class Meta:
        model = hot_list
        fields = '__all__'
        error_messages = {
            "type": {"required": "请选择商品类型"},
            "recentDate": {"required": "请选择日期"},
        }

class HotCommodityForm(forms.ModelForm):
    class Meta:
        model = hot_list
        fields = '__all__'
        # error_messages = {
        #     "assin": {"required": "商品编号不能为空"},
        #     "title": {"required": "请输入商品名称"},
        #     # "present_price": {},
        #     "buyDate": {"required": "请输入购买日期"},
        #     "warrantyDate": {"required": "请输入质保日期"},
        #     "status": {"required": "请选择商品状态"}
        # }

    # def clean(self):
    #     cleaned_data = super(SalesQueryForm, self).clean()
    #     assin = cleaned_data.get("assin")
    #     if sales_counts.objects.filter(assin=assin).count():
    #         raise forms.ValidationError('资产编号：{}已存在'.format(assin))