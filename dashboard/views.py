from django.shortcuts import render
from users.models import Patient


def dashboard(request):
    """Retorna view de dashboard dado patiente selecionado do caregiver logado"""
    # TODO: Aramazenar sessão para identificar caregiver que está logado, e pegar lista
    # de paciente relacionados a ele. Por enquanto, está pegando o primeiro paciente da lista
    patient = Patient.objects.all()[0]
    meds = patient.medication_set.order_by("time")

    context = {
        'patient': patient,
        'meds': meds
    }
    return render(request, 'dashboard.pug', context=context)
