from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Product, Goods

class ApplyForm(forms.Form):
    facility = forms.CharField(
        label='品名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入产品名称'})
    )
    version= forms.CharField(
        label='型号',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入产品型号'})
    )
    number = forms.CharField(
        label='数量',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请申请数量'})
    )


class PriceForm(forms.Form):
    price =forms.CharField(
        label='单价',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入单价'})
    )
    total_price = forms.CharField(
        label='总价',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入总价'})
    )

class Warehouse(forms.Form):
    pass


class ProductForm(forms.Form):
    facility_id = forms.CharField(
        label='设备',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入设备'})
    )
    staff_name = forms.CharField(
        label='员工',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入员工姓名'})
    )
    product_name = forms.CharField(
        label='品名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入品名'})
    )
    today_done_num= forms.CharField(
        label='今日产量',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入今日产量'})
    )
    qualified_num= forms.CharField(
        label='今日合格量',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入今日合格量'})
    )


class ProductDairySelectForm(forms.Form):

    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1,'日期'),(2,'设备'),(3,'员工')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )


class PurchaseListSelectForm(forms.Form):

    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1,'品名'),(2,'申请人'),(3,'批准人'),(4,'采购人')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )


class WarehouseAppendForm(forms.Form):
    products = Product.objects.all()
    posit = []
    for p in products:
        posit.append((p.product_name, p.product_name))
    product_name = forms.CharField(
        label='品名',
        widget=forms.Select(choices=posit)
    )
    number = forms.CharField(
        label='数量',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入数量'})
    )
    unit = forms.CharField(
        label='单位',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入单位'})
    )


class ProductTypeAppendForm(forms.Form):
    product_name = forms.CharField(
        label='品名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入品名'})
    )


class SourceTypeAppendForm(forms.Form):
    good_type = forms.CharField(
        label='品名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入品名'})
    )


class WarehouseSourceAppendForm(forms.Form):
    goods = Goods.objects.all()
    posit = []
    for p in goods:
        posit.append((p.good_name, p.good_name))
    source_name = forms.CharField(
        label='品名',
        widget=forms.Select(choices=posit)
    )
    number = forms.CharField(
        label='数量',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入数量'})
    )
    unit = forms.CharField(
        label='单位',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入单位'})
    )


class WarehouseSelectForm(forms.Form):

    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1,'日期'),(2,'品名')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )
