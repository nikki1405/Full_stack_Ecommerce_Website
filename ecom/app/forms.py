from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    UsernameField, 
    PasswordResetForm,
    PasswordChangeForm  # Fixed capitalization here
)
from .models import Customer, STATE_CHOICES
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MyPasswordChangeForm(PasswordChangeForm):  # Fixed class name
    old_password = forms.CharField(
        label='Old Password', 
        widget=forms.PasswordInput(attrs={
            'autofocus': 'True',
            'autocomplete': 'current-password',
            'class': 'form-control'
        })
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control'
        })
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control'
        })
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    locality = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.ChoiceField(
        choices=STATE_CHOICES,  # Use imported STATE_CHOICES instead of Customer.STATE_CHOICES
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'zipcode', 'state']
