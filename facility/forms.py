from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class BaoxiuForm(forms.Form):
    facility = forms.CharField(
        label='故障设备',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入问题设备编号'})
    )
    question = forms.CharField(
        label='问题描述',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请简述设备的问题'})
    )


class FacilityForm(forms.Form):
    facility_name = forms.CharField(
        label='设备名称',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入设备名称'})
    )
    version = forms.CharField(
        label='设备型号',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入设备型号'})
    )
    price = forms.CharField(
        label='价格',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入设备的价格'})
    )


class FacilitySelectForm(forms.Form):

    keyword = forms.CharField(
        label='关键字',
        widget=forms.Select(choices=((1, '设备名称'), (2, '购买时间'), (3, '购买人'), (4, '购买价格')))

    )
    valueword = forms.CharField(
        label='查找字段',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查找字段'})
    )


class MaintainAppendForm(forms.Form):
    facility_id = forms.CharField(
        label='设备名称',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入设备名称'})
    )
    complmentary = forms.CharField(
        label='保养描述',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入保养描述'})
    )


class MaintainSelectForm(forms.Form):
    keyword = forms.CharField(
        label='关键字',
        widget=forms.Select(choices=((1, '设备名称'), (2, '保养人')))

    )
    valueword = forms.CharField(
        label='查找字段',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查找字段'})
    )


class RepairedSelectForm(forms.Form):
    keyword = forms.CharField(
        label='关键字',
        widget=forms.Select(choices=((1, '设备名称'), (2, '报修人'), (3, '维修人')))

    )
    valueword = forms.CharField(
        label='查找字段',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查找字段'})
    )