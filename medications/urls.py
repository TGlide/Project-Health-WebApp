from django.urls import path

from . import views

app_name = "medications"

urlpatterns = [
    path('meds', views.meds_all, name='meds_all'),
]
