from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notice
from .forms import notice_publishForm
from django.core.mail import send_mail


def notice(request, notice_pk):
    notice = Notice.objects.filter(pk=notice_pk)
    context= {}
    context['notice'] = notice
    return render(request, 'notice.html', context)


def notice_publish(request):
    if request.method == 'POST':
        notice_form = notice_publishForm(request.POST)
        if notice_form.is_valid():
            title = notice_form.cleaned_data['title']
            content = notice_form.cleaned_data['content']
            author = request.user
            add = Notice(title=title, content=content, author=author)
            add.save()
            send_mail('Subject here', '有新通知.', 'liujinhao0519@163.com',
                      ['liujinhao@secrul.cn'], fail_silently=False)
            return redirect(reverse('notice_lists'))
    else:
        notice_form = notice_publishForm()
    context = {}
    context['notice_form'] = notice_form
    return render(request, 'notice_publish.html', context)

def notice_lists(request):
    notice = Notice.objects.all()
    context = {}
    context['notice'] = notice
    return render(request, 'notice_lists.html', context)


def NoticeModify(request, notice_pk):
    usr = request.user
    notc = get_object_or_404(Notice, pk=notice_pk)
    if usr.is_authenticated:
        if request.method == 'POST':
            notice_form = notice_publishForm(request.POST)
            if notice_form.is_valid():
                notc.title = notice_form.cleaned_data['title']
                notc.content = notice_form.cleaned_data['content']
                notc.author = usr
                notc.save()
                return redirect(reverse('notice_lists'))

        notice_form = notice_publishForm(initial={'title':notc.title, 'author':notc.author,'content':notc.content})
        context = {}
        context['notice_form'] = notice_form
        return render(request, 'notice_modify.html', context)
    else:
        return redirect(reverse('login'))


def delete_notice(request,notice_pk):
    usr = request.user
    notc = get_object_or_404(Notice, pk=notice_pk)
    if usr.is_authenticated:
        notc.delete()
        return redirect(reverse('notice_lists'))
    else:
        return redirect(reverse('login'))
