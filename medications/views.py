from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse
from django.http import JsonResponse

from .forms import meds_addForm
from users.models import Caregiver, Patient
from medications.models import Medication
from helpers import logged

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
        form = meds_addForm(request.POST) # Cria form a partir de dados enviados
        if form.is_valid():
            data = form.cleaned_data
            # Add med
            patient =  get_object_or_404(Patient, id=request.session['patient'])
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
            state = ['awaiting','not_taken'][med.past_time()]
        else:
            med.taken = True
            state = 'taken'
        med.save()
        return JsonResponse({'result': 'SUCCESS', 'message': 'yay', 'state': state, 'med_id': med.id})
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
