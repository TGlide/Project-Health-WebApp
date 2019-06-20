from django.shortcuts import render, get_object_or_404
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
