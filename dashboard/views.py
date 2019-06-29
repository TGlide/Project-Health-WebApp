from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from users.models import Patient, Caregiver
from .forms import loginForm, signupForm
from helpers import logged


def dashboard(request):
    """Retorna view de dashboard dado patiente selecionado 
    do caregiver logado"""
    if not logged(request):
        return redirect('dashboard:login')

    caregiver = get_object_or_404(Caregiver, id=request.session['caregiver'])

    patient = None
    meds = []
    foods = []
    if caregiver.has_patients():
        if not 'patient' in request.session:
            patients = caregiver.patient_set.all()
            request.session['patient'] = patients[0].id
        patient = Patient.objects.get(id=request.session['patient'])
        meds = patient.medication_set.order_by("time")
        foods = patient.nutrition_set.order_by("time")

    context = {
        'caregiver': caregiver,
        'patient': patient,
        'meds': meds,
        'foods': foods
    }
    return render(request, 'dashboard.pug', context=context)


def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.pug')

    elif request.method == 'POST':
        form = signupForm(request.POST)  # Cria form a partir de dados enviados

        if form.is_valid():
            data = form.cleaned_data

            # Ve se password == confirm password
            if data['pw'] != data['cpw']:
                return render(request, 'registration/signup.pug', {'wpw': True})

            # Ve se usuario ja existe
            try:
                c = Caregiver.objects.get(email=data['email'])

            except ObjectDoesNotExist:
                # Cria usuário
                c = Caregiver()
                c.email = data['email']
                c.password = data['pw']
                c.name = data['name']
                c.save()
                
                url = reverse('dashboard:login')
                url += '?signup=True'
                return redirect(url)

            # Usuário já existe
            else:
                return render(request, 'registration/signup.pug', {'exists': True})

        else:
            return render(request, 'registration/signup.pug', {'invalid': True})


def login(request):
    context = {
        'signup': False,
        'invalid': False
    }
    if request.method == 'GET':
        context['signup'] = request.GET.get('signup', False)
        return render(request, 'registration/login.pug', context=context)

    elif request.method == 'POST':
        form = loginForm(request.POST)  # Cria form a partir de dados enviados
        if form.is_valid():
            data = form.cleaned_data
            # Tenta fazer login
            try:
                c = Caregiver.objects.get(email=data['email'])
            except ObjectDoesNotExist:
                context['invalid'] = True
                return render(request, 'registration/login.pug', context)
            else:
                if c.password == data['pw']:
                    request.session['caregiver'] = c.id  # Armazena usuário
                    return redirect('dashboard:dashboard')
                context['invalid'] = True
                return render(request, 'registration/login.pug', context)
        else:
            context['invalid'] = True
            return render(request, 'registration/login.pug', context)


def logout(request):
    if 'caregiver' in request.session:
        del request.session['caregiver']
    if 'patient' in request.session:
        del request.session['patient']
    return redirect('dashboard:login')
