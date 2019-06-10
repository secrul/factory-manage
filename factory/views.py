from django.shortcuts import get_object_or_404,redirect,render
from notice.models import Notice



def home(request):
    notices = Notice.objects.all()
    context = {}
    context['notices'] = notices
    return render(request, 'home.html', context)


