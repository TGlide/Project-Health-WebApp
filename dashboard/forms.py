from django import forms


class loginForm(forms.Form):
    email = forms.EmailField()
    pw = forms.CharField()
