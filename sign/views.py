from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from board.models import Resp, Ad


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
