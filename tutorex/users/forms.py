from django import forms
from .models import BaseUser
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
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
        fields = ["first_name", "last_name", "email", "password", "password2", "is_teacher"]


class SignUpParentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    parent_password = forms.CharField(widget=forms.PasswordInput())
    parent_password2 = forms.CharField(widget=forms.PasswordInput())
    birthday = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = BaseUser
        fields = ["first_name", "last_name", "email", "password", "password2", "parent_password", "parent_password2", "is_teacher"]


class UpdateUserDataForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget(), required=False)
    birthday = forms.DateField(widget=forms.DateInput())

    # class Meta:
    #     model = BaseUser
    #     fields = ["first_name", "last_name", "email", "phone_number"]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
