from django import forms


class patient_addForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    age = forms.IntegerField()
