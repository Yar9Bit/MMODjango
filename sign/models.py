from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django.contrib.auth.models import models, User
import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

# Create your models here.


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(unique=True, max_length=128)

    def __str__(self):
        return f'OTP for {self.user}'


@login_required
def send_otp(request):
    code = secrets.token_urlsafe(16)
    send_mail(
        subject='OneTimePassword создан',
        message=code,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email]
    )
    OneTimePassword.objects.create(user=request.user, code=code)
    return redirect('board')


@login_required
def delete_otp(request):
    OneTimePassword.objects.filter(user=request.user).delete()
    send_mail(
        subject='Delete OTP',
        message='Ваш код был автоматически удален',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email]
    )
    return redirect('board')
