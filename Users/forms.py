from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistration(UserCreationForm):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'autocomplete': 'email'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'password'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'password'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserAuthentication(AuthenticationForm):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'autocomplete': 'email'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'autocomplete': 'password'}))
