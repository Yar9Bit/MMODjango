from django.urls import path
from allauth.account.views import LoginView, LogoutView
from .views import RespList, ConfirmUser, ConfirmUserOTP, check_otp, user_change_staff

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/login.html'), name='logout'),
    path('profile/', RespList.as_view(template_name='sign/profile.html'), name='profile'),
    path('confirm/', ConfirmUser.as_view(), name='confirm'),
    path('confirm_user/', ConfirmUserOTP.as_view(), name='confirm_user'),
    path('confirm_otp/', check_otp, name='otp'),
    path('user_staff/', user_change_staff, name='user_staff'),

]
