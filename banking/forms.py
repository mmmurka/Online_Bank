from django.contrib.auth.models import User
from django import forms
from .validator import validate_alpha, validate_min_length_2, validate_password


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100, validators=[validate_alpha, validate_min_length_2])
    last_name = forms.CharField(max_length=100, validators=[validate_alpha, validate_min_length_2])
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, validators=[validate_password])

    def clean_password2(self):
        cd = self.cleaned_data
        if 'password' in cd and 'password2' in cd and cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PaymentForm(forms.Form):
    email = forms.EmailField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
