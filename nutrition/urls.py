from django.urls import path

from . import views

app_name = "nutrition"

urlpatterns = [
    path('foods', views.nutrition_all, name='nutrition_all'),
]
