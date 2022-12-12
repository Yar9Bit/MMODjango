from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic.edit import FormMixin

from .models import Ad, Resp
from .forms import AdForm, RespForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


# Create your views here.


class AdListView(ListView):
    model = Ad
    ordering = '-pk'
    context_object_name = 'ad_list'
    template_name = 'board/ad_list.html'
    paginate_by = 10


class AdDetailView(DetailView, FormMixin):
    model = Ad
    form_class = RespForm
    template_name = 'board/ad_detail.html'
    context_object_name = 'content'


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    template_name = 'board/ad_create.html'

    def get_context_data(self, **kwargs):
        context = super(AdCreate, self).get_context_data(**kwargs)
        context['form'] = AdForm
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.email = User.objects.get(email=self.request.user.email)
        self.object.save()
        return super(AdCreate, self).form_valid(form)


class AdEdit(UpdateView, LoginRequiredMixin):
    model = Ad
    form_class = AdForm
    template_name = 'board/ad_edit.html'


class AdDelete(DeleteView, LoginRequiredMixin):
    model = Ad
    template_name = 'board/ad_delete.html'
    success_url = reverse_lazy('board')


class RespCreate(LoginRequiredMixin, CreateView):
    model = Resp
    form_class = RespForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.post = get_object_or_404(Ad, pk=self.request.POST.get('adId'))
        if self.object.post:
            user = User.objects.all().values().get(pk=self.object.post.author.pk).get('email')
            send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                message=f'Отклик на ваше объявление\n {self.object.post.title}.',
                recipient_list=[user],
                subject='Resp',
            )
        self.object.save()
        return super(RespCreate, self).form_valid(form)
