from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Caregiver, Patient
from .forms import patient_addForm
from helpers import logged


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


def patient_all(request):
    if not logged(request):
        return redirect('dashboard:login')
    c = Caregiver.objects.get(id=request.session['caregiver'])
    context = {
        'patients': c.patient_set.all(),
        'patient_current': request.session['patient']
    }

    return render(request, 'patient_all.pug', context=context)


def patient_change(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    request.session['patient'] = patient.id

    return redirect("users:patient_all")


def patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    context = {
        'patient': patient
    }

    return render(request, 'patient_details.pug', context=context)


def patient_add(request):
    if request.method == 'GET':
        return render(request, 'patient_add.pug')
    elif request.method == 'POST':
        # Cria form a partir de dados enviados
        form = patient_addForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Vê se caregiver está logado
            try:
                c = Caregiver.objects.get(id=request.session['caregiver'])
            except ObjectDoesNotExist:
                return redirect('dashboard:login')
            else:
                # Add paciente
                patient = Patient()
                patient.caregiver = c
                patient.name = data['name']
                patient.email = data['email']
                patient.age = data['age']
                patient.pw = 'not_defined'
                patient.save()

                if 'patient' not in request.session:
                    request.session['patient'] = patient.id

                return redirect('users:patient_all')


# API Views
def api_caregiver(request, caregiver_id):
    # Base response
    response_data = {
        'result': 'SUCCESS',
        'message': None,
        'caregiver': None
    }

    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    response_data['caregiver'] = caregiver.to_dict()
    return JsonResponse(response_data)

def api_caregiver_patients(request, caregiver_id):
    # Base response
    response_data = {
        'result': 'SUCCESS',
        'message': None,
        'patients': []
    }

    caregiver = get_object_or_404(Caregiver, id=caregiver_id)

    for patient in caregiver.patient_set.all():
        response_data['patients'].append(patient.to_dict())

    return JsonResponse(response_data)

def api_patient(request, patient_id):
    # Base response
    response_data = {
        'result': 'SUCCESS',
        'message': None,
        'patient': None
    }

    patient = get_object_or_404(Patient, id=patient_id)
    response_data['result'] = [patient.to_dict()]

    return JsonResponse(response_data)

