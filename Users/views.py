from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegistration, AuthenticationForm
from django.contrib.auth import login, logout


class Registration(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = UserRegistration()
            return render(self.request, 'Users/registration.html', {'form': form})
        else:
            return redirect(self.request.path)

    def post(self, *args, **kwargs):
        form = UserRegistration(self.request.POST, self.request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.photo = self.request.FILES['photo']
            user.save()

            try:
                login(self.request, user)
                messages.success(self.request, 'You successfully created an account!')
            except (Exception,) as a:
                print(a)
                messages.error(self.request, 'Something went wrong. Try again.')

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
            return redirect(self.request.path)

    def post(self, *args, **kwargs):
        form = AuthenticationForm(data=self.request.POST)

        if form.is_valid():
            user = form.get_user()
            login(self.request, user)
            return redirect('customer-account')
        return render(self.request, 'Users/authentication.html', {'form': form})


class Logout(View):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                logout(self.request)
                messages.success(self.request, 'You successfully logged out!')
            except (Exception,) as a:
                print(a)
                messages.error(self.request, 'Something went wrong. Try again.')
        else:
            messages.error(self.request, 'You can\'t logout if you are not authenticated')
        return redirect('authentication')


class UserDetailPage(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('registration')
        else:
            user = self.request.user
            context = {
                'user': user
            }
            return render(self.request, template_name='Users/account.html', context=context)
