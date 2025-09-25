from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField()

class VerifyForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(max_length=6)
