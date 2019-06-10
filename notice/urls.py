from django.urls import path
from . import views


urlpatterns = [
    path('notice/<int:notice_pk>', views.notice, name='notice'),
    path('notice_publish/', views.notice_publish, name='notice_publish'),
    path('notice_lists/', views.notice_lists, name='notice_lists'),
    path('NoticeModify/<int:notice_pk>', views.NoticeModify, name='NoticeModify'),
    path('delete_notice/<int:notice_pk>', views.delete_notice, name='delete_notice'),
]