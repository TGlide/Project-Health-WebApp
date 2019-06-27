from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('caregiver/<int:caregiver_id>', views.caregiver_details, name='caregiver_details'),
    path('patient/<int:patient_id>', views.patient_details, name='patient_details'),
    path('patient/add', views.patient_add, name='patient_add')
]
