from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('caregiver/<int:caregiver_id>', views.caregiver_details, name='caregiver_details'),
    path('patient/all', views.patient_all, name='patient_all'),
    path('patient/change/<int:patient_id>', views.patient_change, name='patient_change'),
    path('patient/<int:patient_id>', views.patient_details, name='patient_details'),
    path('patient/add', views.patient_add, name='patient_add'),
    
    path('api/caregiver/<int:caregiver_id>', views.api_caregiver, name='api_caregiver'),
    path('api/caregiver/patients/<int:caregiver_id>', views.api_caregiver_patients, name='api_caregiver_patients'),
    path('api/patient/<int:patient_id>', views.api_patient, name='api_patient'),
    path('api/patient/meds/<int:patient_id>', views.api_patient_meds, name='api_patient_meds'),
    path('api/patient/foods/<int:patient_id>', views.api_patient_foods, name='api_patient_foods'),
]
