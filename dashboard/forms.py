from django import forms


class loginForm(forms.Form):
    email = forms.EmailField()
    pw = forms.CharField()

class signupForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    pw = forms.CharField()
    cpw = forms.CharField()
