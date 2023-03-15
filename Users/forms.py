from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
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


class UserResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}))


class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New password',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='New password confirmation',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='New email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.all()
        emails_list = []

        for user in users:
            emails_list.append(user.email)

        if email in emails_list:
            self.add_error("email", "This email is already taken!")
        return email
