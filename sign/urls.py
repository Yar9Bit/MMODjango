from django.urls import path
from allauth.account.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/login.html'), name='logout'),

]
