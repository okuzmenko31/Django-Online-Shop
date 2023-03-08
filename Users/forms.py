from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistration(UserCreationForm):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Surname',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'autocomplete': 'email'}))
    photo = forms.ImageField(label='Photo',
                             widget=forms.FileInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label='City',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    post_office = forms.CharField(label='Post office',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'password'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'password'}))

    class Meta:
        model = User
        fields = (
            'name', 'last_name', 'surname', 'phone', 'email', 'photo', 'city', 'post_office', 'password1', 'password2')


class UserAuthentication(AuthenticationForm):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'autocomplete': 'email'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'autocomplete': 'password'}))
