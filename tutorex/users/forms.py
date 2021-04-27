from django import forms
from .models import BaseUser

# class SignUpForm(forms.Form):
#     email = forms.EmailField()
#     name = forms.CharField(max_length=30)
#     lastname = forms.CharField(max_length=100)
#     password = forms.CharField()


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    birthday = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = BaseUser
        fields = ["first_name", "last_name", "email", "password", "password2"]
