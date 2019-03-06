from django import forms
from django.contrib.auth import get_user_model

from .models import WorkOrder

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'mobile']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']
