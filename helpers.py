def logged(request):
    return 'caregiver' in request.session
    