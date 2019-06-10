from django.urls import path
from . import views


urlpatterns = [
    path('order_list/', views.order_list, name='order_list'),
    path('order_modify/<int:order_pk>', views.order_modify, name='order_modify'),
    path('order_delete/<int:order_pk>', views.order_delete, name='order_delete'),
    path('order_append/', views.order_append, name='order_append'),
    path('order_select/', views.order_select, name='order_select'),
]