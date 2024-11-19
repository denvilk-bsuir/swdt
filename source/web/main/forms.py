from django import forms
from django.utils.translation import gettext_lazy as _


class SignUpForm(forms.Form):
    username = forms.CharField(label=_('UsernameField'), max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('PasswordField'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label=_('PasswordConfirmField'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label=_('FirstnameField'), max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label=_('MiddlenameField'),
        max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('LastnameField'), max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label=_('CountryField'), max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_('EmailField'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
