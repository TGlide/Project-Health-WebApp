from django.shortcuts import render


def nutrition_all(request):
    return render(request, 'food_all.pug')
