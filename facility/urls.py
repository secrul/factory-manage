from django.urls import path
from . import views


urlpatterns = [
    path('repaired_select/', views.repaired_select, name='repaired_select'),
    path('facility_document/', views.facility_document, name='facility_document'),
    path('facility_append/', views.facility_append, name='facility_append'),
    path('facility_modify/<int:facility_pk>', views.facility_modify, name='facility_modify'),
    path('facility_delete/<int:facility_pk>', views.facility_delete, name='facility_delete'),
    path('facility_select/', views.facility_select, name='facility_select'),
    path('maintain_document/', views.maintain_document, name='maintain_document'),
    path('maintain_append/', views.maintain_append, name='maintain_append'),
    path('maintain_select/', views.maintain_select, name='maintain_select'),
    path('maintain_modify/<int:maintain_pk>', views.maintain_modify, name='maintain_modify'),
    path('maintain_delete/<int:maintain_pk>', views.maintain_delete, name='maintain_delete'),
    path('baoxiu/<int:user_pk>', views.baoxiu, name='baoxiu'),
    path('baoxiu_list/', views.baoxiu_list, name='baoxiu_list'),
    path('dai_repair/', views.dai_repair, name='dai_repair'),
    path('repaired_list/', views.repaired_list, name='repaired_list'),
    path('mark_done/<int:repair_pk>/<int:user_pk>', views.mark_done, name='mark_done'),
]
