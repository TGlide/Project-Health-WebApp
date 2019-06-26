from django.shortcuts import render

def meds_all(request):
    return render(request, 'meds_all.pug')
