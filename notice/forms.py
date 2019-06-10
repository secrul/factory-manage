from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class notice_publishForm(forms.Form):
    title = forms.CharField(
        label='标题',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入标题'})
    )
    content = forms.CharField(
        label='内容',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入内容'})
    )
