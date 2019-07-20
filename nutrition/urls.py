from django.urls import path

from . import views

app_name = "nutrition"

urlpatterns = [
    path('foods', views.nutrition_all, name='nutrition_all'),
    path('foods/toggle/', views.nutrition_toggle, name='nutritions_toggle'),

    path('api/foods', views.api_foods, name='api_foods'),
]
