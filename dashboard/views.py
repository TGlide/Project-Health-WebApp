from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from users.models import Patient, Caregiver
from .forms import loginForm
from helpers import logged


def dashboard(request):
    """Retorna view de dashboard dado patiente selecionado 
    do caregiver logado"""
    if not logged(request):
        return redirect('dashboard:login') 
    
    caregiver = get_object_or_404(Caregiver, id=request.session['caregiver'])
    
    patient = None
    meds = []
    food = []
    if caregiver.has_patients():
        patients = caregiver.patient_set.all()
        patient = patients[0]
        request.session['patient'] = patient.id
        meds = patient.medication_set.order_by("time")
        foods = patient.nutrition_set.order_by("time")
        
    context = {
        'caregiver': caregiver,
        'patient': patient,
        'meds': meds,
        'foods': foods
    }
    return render(request, 'dashboard.pug', context=context)


def login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.pug')
    
    elif request.method == 'POST':
        form = loginForm(request.POST) # Cria form a partir de dados enviados
        if form.is_valid():
            data = form.cleaned_data
            # Tenta fazer login
            try:
                c = Caregiver.objects.get(email=data['email'])
            except ObjectDoesNotExist:
                return render(request, 'registration/login.pug', {'invalid': True})
            else:
                if c.password == data['pw']:
                    request.session['caregiver'] = c.id # Armazena usuário
                    return redirect('dashboard:dashboard')
                return render(request, 'registration/login.pug', {'invalid': True})
        else:
            return render(request, 'registration/login.pug', {'invalid': True})