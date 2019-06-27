from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Caregiver, Patient


def caregiver_details(request, caregiver_id):
    """Detalhes de um caregiver específico de id=caregiver_id"""
    # Caregiver de id=caregiver_id. Retorna 404 caso não exista.
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    patients = caregiver.patient_set.all()  # Pacientes de caregiver

    context = {
        'caregiver': caregiver,
        'patients': patients
    }

    return render(request, 'caregiver_details.pug', context=context)


def patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    context = {
        'patient': patient
    }

    return render(request, 'patient_details.pug', context=context)


def patient_add(request):
    if request.method == 'GET':
        return render(request, 'patient_add.pug')

# API Views
def api_caregiver(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    response_data = {}
    response_data['result'] = [caregiver.to_dict()]
    return JsonResponse(response_data)

def api_caregiver_patients(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    response_data = {}
    response_data['result'] = []
    for patient in caregiver.patient_set.all():
        response_data['result'].append(patient.to_dict())
    return JsonResponse(response_data)

def api_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    response_data = {}
    response_data['result'] = [patient.to_dict()]
    return JsonResponse(response_data)

def api_patient_meds(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    response_data = {}
    response_data['result'] = []
    for m in patient.medication_set.all():
        response_data['result'].append(m.to_dict())
    return JsonResponse(response_data)

def api_patient_foods(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    response_data = {}
    response_data['result'] = []
    for m in patient.nutrition_set.all():
        response_data['result'].append(m.to_dict())
    return JsonResponse(response_data)

    