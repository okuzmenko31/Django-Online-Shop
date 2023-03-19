from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('authentication/', Authentication.as_view(), name='authentication'),
    path('logout/', Logout.as_view(), name='logout'),
    path('account/', UserDetailPage.as_view(), name='customer-account'),
    path('password-reset/', UserResetPassword.as_view(), name='password-reset'),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(template_name='Users/password-reset-confirmation.html'),
         name='confirmation'),
    path('password-reset/complete/',
         views.PasswordResetDoneView.as_view(template_name='Users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-change/', UserChangePassword.as_view(), name='password-change'),
    path('settings/change-email/', UserChangeEmailView.as_view(), name='change-email'),
    path('my-orders/', UserOrders.as_view(), name='user-orders'),
    path('order-detail/<int:order_id>/', UserOrderDetail.as_view(), name='user-order-detail'),
    path('my-coupons/', UserCoupons.as_view(), name='user-coupons')
]
