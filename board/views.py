from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ad, Resp
from .forms import AdForm
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView

# Create your views here.


class AdListView(ListView):
    model = Ad
    ordering = '-pk'
    context_object_name = 'ad_list'
    template_name = 'board/ad_list.html'
    paginate_by = 10


class AdDetailView(DetailView):
    model = Ad
    template_name = 'board/ad_detail.html'
    context_object_name = 'ad_detail'


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
