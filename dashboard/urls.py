from django.urls import path
from django.conf.urls import url

from . import views

app_name = "dashboard"

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('login/', views.login, name='login'),

]
