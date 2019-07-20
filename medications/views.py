from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from .forms import meds_addForm
from users.models import Caregiver, Patient
from medications.models import Medication
from helpers import logged

import json


def meds_all(request):
    if not logged:
        return redirect('dashboard:login')

    patient = None
    meds = None
    if 'patient' in request.session:
        patient = Patient.objects.get(id=request.session['patient'])
        meds = patient.medication_set.all()

    context = {
        'patient': patient,
        'meds': meds
    }

    return render(request, 'meds_all.pug', context)


def meds_add(request):
    if not logged:
        return redirect('dashboard:login')
    if not 'patient' in request.session:
        return redirect('medications:meds_all')

    if request.method == 'GET':
        return render(request, 'meds_add.pug')

    elif request.method == 'POST':
        # Cria form a partir de dados enviados
        form = meds_addForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Add med
            patient = get_object_or_404(Patient, id=request.session['patient'])
            med = Medication()
            med.name = data['name']
            med.dose = data['dose']
            med.time = data['time']
            med.taken = False
            med.patient = patient
            med.save()

            return redirect('medications:meds_all')
        else:
            return render(request, 'meds_add.pug', {'invalid': True})


def meds_toggle(request):
    if request.method == 'POST':
        if not logged or 'patient' not in request.session:
            return JsonResponse({'result': 'FAIL', 'message': 'error'})

        patient = get_object_or_404(Patient, id=request.session['patient'])
        med = get_object_or_404(Medication, id=request.POST['med_id'])
        if med.patient != patient:
            return JsonResponse({'result': 'FAIL', 'message': 'error'})

        if med.taken:
            med.taken = False
        else:
            med.taken = True
        med.save()
        return JsonResponse({'result': 'SUCCESS', 'message': 'yay', 'state': med.state(), 'med_id': med.id})
    return Http404()


def meds_delete(request, med_id):
    if not logged:
        return redirect('dashboard:login')

    patient = get_object_or_404(Patient, id=request.session['patient'])
    med = get_object_or_404(Medication, id=med_id)
    if med.patient != patient:
        return Http404()
    med.delete()

    return redirect('medications:meds_all')


# API views
@csrf_exempt
def api_meds(request):
    # Request methods
    methods = ["GET", "DELETE", "PUT"]
    if request.method not in methods:
        return Http404

    # Parameters
    params = {
        "patient_id": None,
        "med_id": None,
        "taken": None
    }
    # Base response
    response_data = {
        'result': 'SUCCESS',
        'message': None,
        'meds': []
    }

    # Get the parameters
    if request.method == "GET":
        required = ["patient_id"]

        # GET Parameters
        for key in params.keys():
            params[key] = request.GET.get(key, None)

    elif request.method == "DELETE":
        required = ["patient_id", "med_id"]
        delete_body = json.loads(request.body)

        # DELETE Parameters
        for key in params.keys():
            params[key] = delete_body.get(key)

    elif request.method == "PUT":
        required = ["patient_id", "med_id", "taken"]

        put_body = json.loads(request.body)

        # PUT Parameters
        for key in params.keys():
            params[key] = put_body.get(key)

    # Check if required parameters filled
    if None in [value for key, value in params.items() if key in required]:
        response_data['result'] = "FAIL"
        response_data['message'] = "Missing parameters."
        return JsonResponse(response_data, status=500)

    # Get data
    meds = []
    patient = get_object_or_404(Patient, id=params['patient_id'])

    if params['med_id']:
        meds.append(get_object_or_404(Medication, id=params['med_id']))
        if meds[0].patient != patient:
            response_data['result'] = "FAIL"
            response_data['message'] = "Wrong patient_id <-> med_id combination."
            return JsonResponse(response_data, status=500)
    else:
        for m in patient.medication_set.all():
            meds.append(m.to_dict())

    # Do specific actions based on request method
    if request.method == "GET":
        response_data['meds'] = meds
        return JsonResponse(response_data)

    if request.method == "DELETE":
        response_data['meds'].append(meds[0].to_dict())
        meds[0].delete()
        return JsonResponse(response_data)

    if request.method == "PUT":
        meds[0].taken = params["taken"]
        meds[0].save()
        response_data["meds"].append(meds[0].to_dict())
        return JsonResponse(response_data)
