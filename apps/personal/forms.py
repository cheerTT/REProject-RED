# @Time    : 2019/3/7 21:10
# @Author  : liyuming
# @Remark  : UserUpdateForm ImageUploadForm
from django import forms
from django.contrib.auth import get_user_model

from .models import WorkOrder

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    """
    UserUpdateForm
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'mobile']


class ImageUploadForm(forms.ModelForm):
    """
    ImageUploadForm
    """
    class Meta:
        model = User
        fields = ['image']
