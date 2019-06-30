from django.urls import path

from . import views

app_name = "medications"

urlpatterns = [
    path('meds', views.meds_all, name='meds_all'),
    path('meds/add', views.meds_add, name='meds_add'),
    path('meds/delete/<int:med_id>', views.meds_delete, name='meds_delete'),
]
