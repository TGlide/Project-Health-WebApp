from django import forms


class meds_addForm(forms.Form):
    name = forms.CharField()
    dose = forms.CharField()
    time = forms.TimeField()
