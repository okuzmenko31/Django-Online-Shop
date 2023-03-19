from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.contrib import messages
from django.views.generic import ListView

from Coupons.models import Coupons
from .forms import UserRegistration, AuthenticationForm, UserResetPasswordForm, UserChangePasswordForm, ChangeEmailForm
from django.contrib.auth import login, logout, get_user_model
from .tasks import send_password_reset_mail, change_email_success_mail
from .services import get_clean_email
from Order.models import Order, OrderItem

User = get_user_model()


class Registration(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = UserRegistration()
            return render(self.request, 'Users/registration.html', {'form': form})
        else:
            return redirect('customer-account')

    def post(self, *args, **kwargs):
        form = UserRegistration(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = get_clean_email(form.cleaned_data['email'])
            # get_clean_email returns email without all symbols after @
            user.save()

            try:
                login(self.request, user)
                messages.success(self.request, 'You successfully created an account!')
            except (Exception,):
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
        else:
            messages.error(self.request, 'Login or password is wrong')
        return render(self.request, 'Users/authentication.html', {'form': form})


class Logout(View):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                logout(self.request)
                messages.success(self.request, 'You successfully logged out!')
            except (Exception,):
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


class UserResetPassword(View):

    def get(self, *args, **kwargs):
        reset_form = UserResetPasswordForm()
        return render(self.request, 'Users/password_reset_page.html', {'reset_form': reset_form})

    def post(self, *args, **kwargs):
        reset_form = UserResetPasswordForm(self.request.POST)

        if reset_form.is_valid():
            email = reset_form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)

                if user:
                    subject = 'Requested password reset'
                    email_template_name = 'Users/password_reset_mail_template.html'
                    cont = {
                        'email': email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'OnlineShop',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    msg_html = render_to_string(email_template_name, cont)
                    send_password_reset_mail.delay(subject, email, msg_html)
                    messages.success(self.request, 'Mail was sent successfully!')
            except (Exception,):
                messages.error(self.request, 'User with this email does not exist!')

        return render(self.request, 'Users/password_reset_page.html', {'reset_form': reset_form})


class UserChangePassword(View):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = self.request.user
            form = UserChangePasswordForm(user=user)
            return render(self.request, 'Users/password-change.html', {'form': form})
        else:
            return redirect('registration')

    def post(self, *args, **kwargs):
        user = self.request.user
        form = UserChangePasswordForm(data=self.request.POST, user=user)

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(self.request, 'You successfully changed your password!')
        return render(self.request, 'Users/password-change.html', {'form': form})


class UserChangeEmailView(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, *args, **kwargs):
        form = ChangeEmailForm()
        context = {
            'form': form
        }
        return render(self.request, template_name='Users/user-change-email.html', context=context)

    def post(self, *args, **kwargs):
        user = self.request.user
        form = ChangeEmailForm(self.request.POST)

        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()

            change_email_success_mail.delay(user.username, user.email)
            messages.success(self.request, 'Mail has been successfully changed, please, confirm it.')
        return render(self.request, 'Users/user-change-email.html', {'user': user, 'form': form})


class UserOrders(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'Users/user-orders.html'
    context_object_name = 'orders'
    login_url = 'registration'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, paid=True)


class UserOrderDetail(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'], paid=True)
        order_items = OrderItem.objects.filter(order=order).select_related('product__main_category',
                                                                           'product__subcategory')

        context = {
            'order': order,
            'order_items': order_items
        }
        return render(self.request, template_name='Users/user-order-detail.html', context=context)


class UserCoupons(LoginRequiredMixin, View):
    login_url = 'registration'

    def get(self, *args, **kwargs):
        coupons = Coupons.objects.filter(user=self.request.user)

        context = {
            'coupons': coupons
        }
        return render(self.request, template_name='Users/user-coupons.html', context=context)
