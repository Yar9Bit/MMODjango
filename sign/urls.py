from django.urls import path
from allauth.account.views import LoginView, LogoutView
from .views import RespList

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/login.html'), name='logout'),
    path('profile/', RespList.as_view(template_name='sign/profile.html'), name='profile')

]
