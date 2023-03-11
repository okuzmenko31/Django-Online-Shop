from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from .forms import UserRegistration, AuthenticationForm
from .models import User
from django.contrib.auth import login


class Registration(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = UserRegistration()
            return render(self.request, 'Users/registration.html', {'form': form})
        else:
            return redirect('all_products')

    def post(self, *args, **kwargs):
        form = UserRegistration(self.request.POST, self.request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.photo = self.request.FILES['photo']
            user.save()
            login(self.request, user)

            self.request.user.username = f'user{self.request.user.id}'
            self.request.user.save()
            return redirect('all_products')
        return render(self.request, 'Users/registration.html', {'form': form})


class Authentication(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = AuthenticationForm()
            return render(self.request, 'Users/authentication.html', {'form': form})
        else:
            return redirect('all_products')

    def post(self, *args, **kwargs):
        form = AuthenticationForm(data=self.request.POST)

        if form.is_valid():
            user = form.get_user()
            login(self.request, user)
            return redirect('all_products')
        return render(self.request, 'Users/authentication.html', {'form': form})


class UserDetailPage(View):

    def get(self, *args, **kwargs):
        user = self.request.user
        context = {
            'user': user
        }
        return render(self.request, template_name='Users/detail-page.html', context=context)
