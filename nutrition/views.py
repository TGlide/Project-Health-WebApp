from django.http import JsonResponse, Http404
from django.shortcuts import render

from users.models import Patient, Caregiver
from nutrition.models import Nutrition

def nutrition_all(request):
    return render(request, 'food_all.pug')


def nutrition_toggle(request):
    if request.method == 'POST':
        if not logged or 'patient' not in request.session:
            return JsonResponse({'result': 'FAIL', 'message': 'error'})
        
        patient = get_object_or_404(Patient, id=request.session['patient'])
        food = get_object_or_404(Nutrition, id=request.POST['food_id'])
        if food.patient != patient:
            return JsonResponse({'result': 'FAIL', 'message': 'error'})

        food.taken = [True, False][food.taken]
        food.save()

        return JsonResponse({'result': 'SUCCESS', 'message': 'yay', 'state': food.state(), 'food_id': food.id})
    return Http404()