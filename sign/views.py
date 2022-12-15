import secrets

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from board.models import Resp, Ad
from sign.models import OneTimePassword


class RespList(LoginRequiredMixin, ListView):
    """Authorized user only"""
    model = Resp
    context_object_name = 'responses'
    template_name = 'sign/resp_check.html'
    ordering = '-pk'
    paginate_by = 3

    def get_queryset(self):
        """
        Fetching Queryset to filter ads
        """
        try:
            self.ad = int(self.request.GET.get('ad', 0))
        except ValueError:
            self.ad = 0
        self.user = get_object_or_404(User, id=self.request.user.id)
        queryset = Resp.objects.filter(
            post__in=Ad.objects.filter(author=self.user, pk=self.ad)
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RespList, self).get_context_data(**kwargs)
        context['adverts'] = Ad.objects.filter(author=self.user)
        context['advert_list'] = Ad.objects.filter(author=self.user, pk=self.ad)
        context['ad'] = self.ad
        return context


class ConfirmUser(ListView):
    model = User
    template_name = 'sign/profile.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ConfirmUser, self).get_context_data(**kwargs)
        user_staff = User.objects.all().filter(is_staff=False)
        context['confirm'] = user_staff
        return context


class ConfirmUserOTP(ListView):
    model = OneTimePassword
    template_name = 'sign/email_confirm.html'
    context_object_name = 'otp'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConfirmUserOTP, self).get_context_data(**kwargs)
        return context


@login_required
def resp_change_status(request):
    if request.method == 'POST':
        response = Resp.objects.get(pk=request.POST.get('respId'))
        response.status = True
        response.save(update_fields=['status'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_response(request):
    if request.method == 'POST':
        response = Resp.objects.get(pk=request.POST.get('respId'))
        response.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def check_otp(request):
    otp = OneTimePassword.objects.all().filter(user=request.user.id)
    if not otp.exists():
        return redirect('send_otp')
    return redirect('confirm_user')


@login_required
def user_change_staff(request):
    if request.method == 'POST':
        otp = OneTimePassword.objects.get(user_id=request.user.pk)
        otp.code = request.POST.get('OTPCode')
        staff = User.objects.get(pk=request.user.pk)
        staff.is_staff = True
        staff.save(update_fields=['is_staff'])
    return redirect('profile')


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
    return redirect('otp')
