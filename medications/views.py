from django.shortcuts import render, redirect
from django.http import JsonResponse
from users.models import Caregiver, Patient
from helpers import logged

def meds_all(request):
    if not logged:
        return redirect('dashboard:login')
    caregiver = Caregiver.objects.get(id=request.session['caregiver'])
    
    return render(request, 'meds_all.pug')

# API views
