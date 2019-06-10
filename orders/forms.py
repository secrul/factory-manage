from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import widgets
from warehouse.models import Product

class OrderForm(forms.Form):
    ps = Product.objects.all()
    prod = []
    for p in ps:
        prod.append((p.product_name, p.product_name))
    order_name = forms.CharField(
        label='产品名称',
        widget=forms.Select(choices=prod),
    )
    order_client= forms.CharField(
        label='客户名称',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入客户名称'})
    )
    order_number= forms.CharField(
        label='产品数量',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入产品数量'})
    )
    order_price = forms.CharField(
        label='单价',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入单价'})
    )
    order_total_price = forms.CharField(
        label='总价',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入总价'})
    )
    order_end = forms.DateField(
        label='交货时间',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入交货时间'})
    )
    order_supplement  = forms.CharField(
        label='详细要求',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入详细要求'})
    )


class OrderSelectForm(forms.Form):
    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1, '产品名称'), (2, '客户名称')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )