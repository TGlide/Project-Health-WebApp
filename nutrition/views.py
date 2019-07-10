from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from users.models import Patient, Caregiver
from nutrition.models import Nutrition

import json

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


# API views
@csrf_exempt
def api_foods(request):
    # Request methods
    methods = ["GET", "DELETE", "PUT"]
    if request.method not in methods:
        return Http404

    # Parameters
    params = {
        "patient_id": None,
        "food_id": None,
        "taken": None
    }
    # Base response
    response_data = {
        'result': 'SUCCESS',
        'message': None,
        'foods': []
    }

    # Get the parameters
    if request.method == "GET":
        required = ["patient_id"]

        # GET Parameters
        for key in params.keys():
            params[key] = request.GET.get(key, None)

    elif request.method == "DELETE":
        required = ["patient_id", "food_id"]
        delete_body = json.loads(request.body)

        # DELETE Parameters
        for key in params.keys():
            params[key] = delete_body.get(key)

    elif request.method == "PUT":
        required = ["patient_id", "food_id", "taken"]

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
    foods = []
    patient = get_object_or_404(Patient, id=params['patient_id'])

    if params['food_id']:
        foods.append(get_object_or_404(Nutrition, id=params['food_id']))
        if foods[0].patient != patient:
            response_data['result'] = "FAIL"
            response_data['message'] = "Wrong patient_id <-> food_id combination."
            return JsonResponse(response_data, status=500)
    else:
        for m in patient.nutrition_set.all():
            foods.append(m.to_dict())

    # Do specific actions based on request method
    if request.method == "GET":
        response_data['foods'] = foods
        return JsonResponse(response_data)

    if request.method == "DELETE":
        response_data['foods'].append(foods[0].to_dict())
        foods[0].delete()
        return JsonResponse(response_data)

    if request.method == "PUT":
        foods[0].eaten = params["taken"]
        foods[0].save()
        response_data["foods"].append(foods[0].to_dict())
        return JsonResponse(response_data)
