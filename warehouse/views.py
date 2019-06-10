from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, ProduceDiary, Warehouse,PurchaseList, Goods, WarehouseSource
from facility.models import Facility
from .forms import ApplyForm, PriceForm, ProductForm, ProductDairySelectForm, PurchaseListSelectForm, \
    WarehouseAppendForm, ProductTypeAppendForm, SourceTypeAppendForm,WarehouseSourceAppendForm, WarehouseSelectForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail


def product_diary(request):
    context = {}
    product_diaries = ProduceDiary.objects.all()
    context['product_diaries'] = product_diaries
    return render(request, 'product_diary.html', context)


def warehouse_diary(request):
    context = {}
    warehouse_diaries = Warehouse.objects.all()
    context['warehouse_diaries'] = warehouse_diaries
    return render(request, 'warehouse_diary.html', context)


def apply(request,user_pk):
    ur =get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        apply_form = ApplyForm(request.POST)
        if apply_form.is_valid():
            version = apply_form.cleaned_data['version']
            facility = apply_form.cleaned_data['facility']
            number = apply_form.cleaned_data['number']
            add = PurchaseList(good_name=facility, good_version=version, good_num=number, apply_staff_name=ur)
            add.save()
            send_mail('Subject here', '有一个采购申请请您批准.', 'liujinhao0519@163.com',
                      ['liujinhao@secrul.cn'], fail_silently=False)
            return redirect(reverse('home'))
    else:
        apply_form  = ApplyForm()
    context = {}
    context['apply_form'] = apply_form
    return render(request, 'apply.html', context)


def sanction_list(request):
    purchaselists = PurchaseList.objects.filter(sanction_staff_name=None)
    context = {}
    context['count'] = purchaselists.count()
    context['purchaselists'] = purchaselists
    return render(request, 'sanction_list.html', context)


def sanction(request, apply_pk, user_pk):
    user = request.user
    if user.is_authenticated:
        ur = get_object_or_404(User, pk=user_pk)
        apply_tem = PurchaseList.objects.get(pk=apply_pk)
        apply_tem.sanction_staff_name = ur
        apply_tem.save()
        send_mail('Subject here', '有一个采购申请请您处理.', 'liujinhao0519@163.com',
                  ['liujinhao@secrul.cn'], fail_silently=False)
        return redirect(reverse('sanction_list'))
    else:
        return redirect(reverse('login'))


def buy_list(request):
    purchaselists = PurchaseList.objects.filter(~Q(sanction_staff_name=None), Q(buyer_name=None) )
    context = {}
    context['count'] = purchaselists.count()
    context['purchaselists'] = purchaselists
    return render(request, 'buy_list.html', context)


def price(request,apply_pk, user_pk):
    ur =get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        price_form = PriceForm(request.POST)
        if price_form.is_valid():
            price = price_form.cleaned_data['price']
            total_price = price_form.cleaned_data['total_price']
            apply_tem = PurchaseList.objects.get(pk=apply_pk)
            apply_tem.price = price
            apply_tem.total_price = total_price
            apply_tem.buyer_name = ur
            apply_tem.save()
            good_tem = Goods.objects.filter(good_name=apply_tem.good_name)
            if not good_tem:
                add = Goods(good_name = apply_tem.good_name)
                add.save()
            return redirect(reverse('buy_list'))
    else:
        price_form  = PriceForm()
    context = {}
    context['price_form'] = price_form
    return render(request, 'price.html', context)


def buyed_list(request):
    purchaselists = PurchaseList.objects.filter(~Q(buyer_name=None))
    context = {}
    context['count'] = purchaselists.count()
    context['purchaselists'] = purchaselists
    return render(request, 'buyed_list.html', context)


def product_diary_append(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            ProductForms = ProductForm(request.POST)
            if ProductForms.is_valid():
                facility_id = ProductForms.cleaned_data['facility_id']
                facility_tem = Facility.objects.get(facility_name=facility_id)
                staff_name = ProductForms.cleaned_data['staff_name']
                user_tem = User.objects.get(username = staff_name)
                product_name = ProductForms.cleaned_data['product_name']
                product_tem = Product.objects.get(product_name=product_name)
                today_done_num = ProductForms.cleaned_data['today_done_num']
                qualified_num = ProductForms.cleaned_data['qualified_num']
                add = ProduceDiary(facility_id=facility_tem, staff_name=user_tem, product_name=product_tem,
                             today_done_num=today_done_num,     qualified_num=qualified_num)
                add.save()
                return redirect(reverse('product_diary'))
        else:
            ProductForms = ProductForm()
            context = {}
            context['ProductForms'] = ProductForms
            return render(request, 'product_diary_append.html', context)
    else:
        return redirect(reverse('login'))


def product_diary_delete(request, product_diary_pk):
    usr = request.user
    if usr.is_authenticated:
        order_tem = ProduceDiary.objects.get(pk=product_diary_pk)
        order_tem.delete()
        return redirect(reverse('product_diary'))
    else:
        return redirect(reverse('login'))


def product_diary_modify(request, product_diary_pk):
    usr = request.user
    if usr.is_authenticated:
        product_diary_tem = ProduceDiary.objects.get(pk=product_diary_pk)
        if request.method == 'POST':
            ProductForms = ProductForm(request.POST)
            if ProductForms.is_valid():
                facility_tem = Facility.objects.get(facility_name=ProductForms.cleaned_data['facility_id'])
                product_diary_tem.facility_id = facility_tem
                user_tem = User.objects.get(username=ProductForms.cleaned_data['staff_name'])
                product_diary_tem.staff_name = user_tem
                product_tem = Product.objects.get(product_name=ProductForms.cleaned_data['product_name'])
                product_diary_tem.product_name = product_tem
                product_diary_tem.today_done_num = ProductForms.cleaned_data['today_done_num']
                product_diary_tem.qualified_num = ProductForms.cleaned_data['qualified_num']
                product_diary_tem.save()
                return redirect(reverse('product_diary'))
        else:
            ProductForms = ProductForm(initial={'facility_id':product_diary_tem.facility_id, 'staff_name':product_diary_tem.staff_name,
                                                 'product_name':product_diary_tem.product_name, 'today_done_num':product_diary_tem.today_done_num,
                                                 'qualified_num':product_diary_tem.qualified_num})
            context = {}
            context['ProductForms'] = ProductForms
            return render(request, 'product_diary_append.html', context)
    else:
        return redirect(reverse('login'))


def product_diary_select(request):

    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            ProductDairySelectForms = ProductDairySelectForm(request.POST)
            if ProductDairySelectForms.is_valid():
                keyword = ProductDairySelectForms.cleaned_data['keyword']
                valueword = ProductDairySelectForms.cleaned_data['valueword']
                ans_tem = []
                print(keyword, valueword)
                if keyword == '1':#时间
                    ans_tem = ProduceDiary.objects.filter(current_time__contains=valueword)

                if keyword == '2':#设备
                    ans_tem1 = Facility.objects.filter(Q(facility_name__contains=valueword))
                    ans_tem = ProduceDiary.objects.filter(facility_id__in=ans_tem1)

                if keyword == '3':#员工
                    ans_tem1 = User.objects.filter(Q(username__contains=valueword))
                    ans_tem = ProduceDiary.objects.filter(staff_name__in=ans_tem1)

                context = {}
                context['product_diaries'] = ans_tem
                return render(request, 'product_diary.html', context)
        else:
            ProductDairySelectForms = ProductDairySelectForm()
            context = {}
            context['ProductDairySelectForms'] = ProductDairySelectForms
            return render(request, 'product_diary_select.html', context)
    else:
        return redirect(reverse('login'))


def purchaseList_select(request):

    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            PurchaseListSelectForms = PurchaseListSelectForm(request.POST)
            if PurchaseListSelectForms.is_valid():
                keyword = PurchaseListSelectForms.cleaned_data['keyword']
                valueword = PurchaseListSelectForms.cleaned_data['valueword']
                ans_tem = []
                print(keyword, valueword)
                if keyword == '1':#品名
                    ans_tem = PurchaseList.objects.filter(Q(good_name__contains=valueword),~Q(buyer_name=None))

                if keyword == '2':#申请人
                    ans_tem1 = User.objects.filter(Q(username__contains=valueword))
                    ans_tem = PurchaseList.objects.filter(Q(apply_staff_name__in=ans_tem1),~Q(buyer_name=None))

                if keyword == '3':#批准人
                    ans_tem1 = User.objects.filter(Q(username__contains=valueword))
                    ans_tem = PurchaseList.objects.filter(Q(sanction_staff_name__in=ans_tem1),~Q(buyer_name=None))

                if keyword == '4':#采购人
                    ans_tem1 = User.objects.filter(Q(username__contains=valueword))
                    ans_tem = PurchaseList.objects.filter(buyer_name__in=ans_tem1)

                context = {}
                context['purchaselists'] = ans_tem
                return render(request, 'buyed_list.html', context)
        else:
            PurchaseListSelectForms = PurchaseListSelectForm()
            context = {}
            context['PurchaseListSelectForms'] = PurchaseListSelectForms
            return render(request, 'purchaselist_select.html', context)
    else:
        return redirect(reverse('login'))


def warehouse_append(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            WarehouseAppendForms = WarehouseAppendForm(request.POST)
            if WarehouseAppendForms.is_valid():
                print('cece')
                product_name = WarehouseAppendForms.cleaned_data['product_name']
                facility_tem = Product.objects.get(product_name=product_name)
                number = WarehouseAppendForms.cleaned_data['number']
                unit = WarehouseAppendForms.cleaned_data['unit']
                print(facility_tem,number,unit)
                add = Warehouse(product_name=facility_tem, number=number, unit=unit)
                add.save()
                return redirect(reverse('warehouse_diary'))
            else:
                return redirect(reverse('home'))
        else:
            WarehouseAppendForms = WarehouseAppendForm()
            context = {}
            context['WarehouseAppendForms'] = WarehouseAppendForms
            return render(request, 'warehouse_diary_append.html', context)
    else:
        return redirect(reverse('login'))


def product_list(request):
    products = Product.objects.all()

    context = {}
    context['products'] = products
    return render(request, 'product_list.html', context)


def source_list(request):
    goods = Goods.objects.all()

    context = {}
    context['goods'] = goods
    return render(request, 'source_list.html', context)


def source_diary(request):
    context = {}
    source_diaries = WarehouseSource.objects.all()
    context['source_diaries'] = source_diaries
    return render(request, 'source_diary.html', context)


def productTypeAppend(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            ProductTypeAppendForms = ProductTypeAppendForm(request.POST)
            if ProductTypeAppendForms.is_valid():
                product_name = ProductTypeAppendForms.cleaned_data['product_name']

                add = Product(product_name=product_name)
                add.save()
                return redirect(reverse('product_list'))
            else:
                return redirect(reverse('home'))
        else:
            ProductTypeAppendForms = ProductTypeAppendForm()
            context = {}
            context['ProductTypeAppendForms'] = ProductTypeAppendForms
            return render(request, 'product_type_append.html', context)
    else:
        return redirect(reverse('login'))


def sourceTypeAppend(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            SourceTypeAppendForms = SourceTypeAppendForm(request.POST)
            if SourceTypeAppendForms.is_valid():
                good_type = SourceTypeAppendForms.cleaned_data['good_type']

                add = Goods(good_name=good_type)
                add.save()
                return redirect(reverse('source_list'))
            else:
                return redirect(reverse('home'))
        else:
            SourceTypeAppendForms = SourceTypeAppendForm()
            context = {}
            context['SourceTypeAppendForms'] = SourceTypeAppendForms
            return render(request, 'source_type_append.html', context)
    else:
        return redirect(reverse('login'))


def warehouse_source_append(request):
    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            WarehouseSourceAppendForms = WarehouseSourceAppendForm(request.POST)
            if WarehouseSourceAppendForms.is_valid():
                print('cece')
                source_name = WarehouseSourceAppendForms.cleaned_data['source_name']
                good_tem = Goods.objects.get(good_name=source_name)
                number = WarehouseSourceAppendForms.cleaned_data['number']
                unit = WarehouseSourceAppendForms.cleaned_data['unit']
                print(good_tem,number,unit)
                add = WarehouseSource(source_name=good_tem, number=number, unit=unit)
                add.save()
                return redirect(reverse('source_diary'))
            else:
                return redirect(reverse('home'))
        else:
            WarehouseSourceAppendForms = WarehouseSourceAppendForm()
            context = {}
            context['WarehouseSourceAppendForms'] = WarehouseSourceAppendForms
            return render(request, 'warehouse_source_diary_append.html', context)
    else:
        return redirect(reverse('login'))


def product_type_modify(request, product_type_pk):
    usr = request.user
    if usr.is_authenticated:
        product_type_tem = Product.objects.get(pk=product_type_pk)
        if request.method == 'POST':
            ProductTypeAppendForms = ProductTypeAppendForm(request.POST)
            if ProductTypeAppendForms.is_valid():
                product_type_tem.product_name = ProductTypeAppendForms.cleaned_data['product_name']
                product_type_tem.save()
                return redirect(reverse('product_list'))
        else:
            ProductTypeAppendForms = ProductTypeAppendForm(initial={'product_name':product_type_tem.product_name})
            context = {}
            context['ProductTypeAppendForms'] = ProductTypeAppendForms
            return render(request, 'product_type_append.html', context)
    else:
        return redirect(reverse('login'))


def product_type_delete(request, product_type_pk):
    usr = request.user
    if usr.is_authenticated:
        product_type_tem = Product.objects.get(pk=product_type_pk)
        product_type_tem.delete()
        return redirect(reverse('product_list'))

    else:
        return redirect(reverse('login'))


def good_type_modify(request, good_type_pk):
    usr = request.user
    if usr.is_authenticated:
        good_type_tem = Goods.objects.get(pk=good_type_pk)
        if request.method == 'POST':
            SourceTypeAppendForms = SourceTypeAppendForm(request.POST)
            if SourceTypeAppendForms.is_valid():
                good_type_tem.good_name = SourceTypeAppendForms.cleaned_data['good_type']
                good_type_tem.save()
                return redirect(reverse('source_list'))
        else:
            SourceTypeAppendForms = SourceTypeAppendForm(initial={'good_type':good_type_tem.good_name})
            context = {}
            context['SourceTypeAppendForms'] = SourceTypeAppendForms
            return render(request, 'source_type_append.html', context)
    else:
        return redirect(reverse('login'))


def good_type_delete(request, good_type_pk):
    usr = request.user
    if usr.is_authenticated:
        goods_type_tem = Goods.objects.get(pk=good_type_pk)
        goods_type_tem.delete()
        return redirect(reverse('source_list'))

    else:
        return redirect(reverse('login'))


def warehouse_diary_modify(request, warehouse_pk):
    usr = request.user
    if usr.is_authenticated:
        product_diary_tem = Warehouse.objects.get(pk=warehouse_pk)
        if request.method == 'POST':
            WarehouseAppendForms = WarehouseAppendForm(request.POST)
            if WarehouseAppendForms.is_valid():
                product_diary_tem.product_name = Product.objects.get(product_name=WarehouseAppendForms.cleaned_data['product_name'])
                product_diary_tem.number = WarehouseAppendForms.cleaned_data['number']
                product_diary_tem.unit = WarehouseAppendForms.cleaned_data['unit']
                product_diary_tem.save()
                return redirect(reverse('warehouse_diary'))
        else:
            WarehouseAppendForms = WarehouseAppendForm(initial={'product_name': product_diary_tem.product_name,
                                                                'number':product_diary_tem.number,
                                                                'unit':product_diary_tem.unit})
            context = {}
            context['WarehouseAppendForms'] = WarehouseAppendForms
            return render(request, 'warehouse_diary_append.html', context)
    else:
        return redirect(reverse('login'))


def warehouse_diary_delete(request, warehouse_pk):
    usr = request.user
    if usr.is_authenticated:
        product_diary_tem = Warehouse.objects.get(pk=warehouse_pk)
        product_diary_tem.delete()
        return redirect(reverse('warehouse_diary'))
    else:
        return redirect(reverse('login'))


def warehouse_source_diary_modify(request, warehouse_pk):
    usr = request.user
    if usr.is_authenticated:
        good_diary_tem = WarehouseSource.objects.get(pk=warehouse_pk)
        if request.method == 'POST':
            WarehouseSourceAppendForms = WarehouseSourceAppendForm(request.POST)
            if WarehouseSourceAppendForms.is_valid():
                good_diary_tem.source_name = Goods.objects.get(good_name=WarehouseSourceAppendForms.cleaned_data['source_name'])
                good_diary_tem.number = WarehouseSourceAppendForms.cleaned_data['number']
                good_diary_tem.unit = WarehouseSourceAppendForms.cleaned_data['unit']
                good_diary_tem.save()
                return redirect(reverse('source_diary'))
        else:
            WarehouseSourceAppendForms = WarehouseSourceAppendForm(initial={'source_name': good_diary_tem.source_name,
                                                                'number':good_diary_tem.number,
                                                                'unit':good_diary_tem.unit})
            context = {}
            context['WarehouseSourceAppendForms'] = WarehouseSourceAppendForms
            return render(request, 'warehouse_source_diary_append.html', context)
    else:
        return redirect(reverse('login'))


def warehouse_source_diary_delete(request, warehouse_pk):
    usr = request.user
    if usr.is_authenticated:
        good_diary_tem = WarehouseSource.objects.get(pk=warehouse_pk)
        good_diary_tem.delete()
        return redirect(reverse('source_diary'))
    else:
        return redirect(reverse('login'))


def warehouse_diary_select(request):

    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            WarehouseSelectForms = WarehouseSelectForm(request.POST)
            if WarehouseSelectForms.is_valid():
                keyword = WarehouseSelectForms.cleaned_data['keyword']
                valueword = WarehouseSelectForms.cleaned_data['valueword']
                ans_tem = []
                print(keyword, valueword)
                if keyword == '1':#时间
                    ans_tem = Warehouse.objects.filter(current_time__contains=valueword)

                if keyword == '2':#品名
                    ans_tem1 = Product.objects.filter(Q(product_name__contains=valueword))
                    ans_tem = Warehouse.objects.filter(product_name__in=ans_tem1)

                context = {}
                context['warehouse_diaries'] = ans_tem
                return render(request, 'warehouse_diary.html', context)
        else:
            WarehouseSelectForms = WarehouseSelectForm()
            context = {}
            context['WarehouseSelectForms'] = WarehouseSelectForms
            return render(request, 'warehouse_select.html', context)
    else:
        return redirect(reverse('login'))


def warehouse_source_diary_select(request):

    usr = request.user
    if usr.is_authenticated:
        if request.method == 'POST':
            WarehouseSelectForms = WarehouseSelectForm(request.POST)
            if WarehouseSelectForms.is_valid():
                keyword = WarehouseSelectForms.cleaned_data['keyword']
                valueword = WarehouseSelectForms.cleaned_data['valueword']
                ans_tem = []
                print(keyword, valueword)
                if keyword == '1':#时间
                    ans_tem = WarehouseSource.objects.filter(current_time__contains=valueword)

                if keyword == '2':#品名
                    ans_tem1 = Goods.objects.filter(Q(good_name__contains=valueword))
                    ans_tem = WarehouseSource.objects.filter(source_name__in=ans_tem1)

                context = {}
                context['source_diaries'] = ans_tem
                return render(request, 'source_diary.html', context)
        else:
            WarehouseSelectForms = WarehouseSelectForm()
            context = {}
            context['WarehouseSelectForms'] = WarehouseSelectForms
            return render(request, 'warehouse_source_select.html', context)
    else:
        return redirect(reverse('login'))