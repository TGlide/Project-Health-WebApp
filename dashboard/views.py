from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from users.models import Patient, Caregiver
from .forms import loginForm


def dashboard(request):
    """Retorna view de dashboard dado patiente selecionado 
    do caregiver logado"""
    # TODO: Aramazenar sessão para identificar caregiver que está logado,
    # e pegar listade paciente relacionados a ele. Por enquanto, está pegando
    # o primeiro paciente da lista
    patient = Patient.objects.all()
    if len(patient) > 0:
        patient = patient[0]
        meds = patient.medication_set.order_by("time")
    else:
        patient = None
        meds = []
    context = {
        'patient': patient,
        'meds': meds
    }
    return render(request, 'dashboard.pug', context=context)


def login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.pug')
    elif request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                c = Caregiver.objects.get(email=data['email'])
            except ObjectDoesNotExist:
                return render(request, 'registration/login.pug', {'invalid': True})
            else:
                if c.password == data['pw']:
                    return redirect(dashboard)
                return render(request, 'registration/login.pug', {'invalid': True})
        else:
            return render(request, 'registration/login.pug', {'invalid': True})