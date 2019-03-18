from django import forms
from commodity.models import Commodity, CommodityType, Commodity_price


class CommodityCreateForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ['assin','status']

        error_messages = {
            "assin": {"required": "商品编号不能为空"},
            "status": {"required": "请选择商品状态"},
            # "imUrl":{"required":"请选择图片"}
        }

    def clean(self):
        cleaned_data = super(CommodityCreateForm, self).clean()
        assin = cleaned_data.get("assin")

        if Commodity.objects.filter(assin=assin).count():
            raise forms.ValidationError('资产编号：{}已存在'.format(assin))



class CommodityUpdateForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = '__all__'
        error_messages = {
            "assin": {"required": "商品编号不能为空"},
            "title": {"required": "请输入商品名称"},
            # "present_price": {},
            "buyDate": {"required": "请输入购买日期"},
            "warrantyDate": {"required": "请输入质保日期"},
            "status": {"required": "请选择商品状态"}
        }
#
# class ImageUploadForm(forms.ModelForm):
#     class Meta:
#         model = Commodity
#         fields = ['imUrl']
