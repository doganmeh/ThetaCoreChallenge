from urllib.error import URLError

from django.contrib import messages
from django.shortcuts import render
from django.views import generic

from expert import models


#  parent view classes #############################################################################
def get_return_url(request):
    """
    for generic use; get "next" if available in GET, otherwise HTTP_REFERER
    """
    if 'next' in request.GET:
        return request.GET.get('next')
    return request.META.get('HTTP_REFERER')


class ListView(generic.ListView):
    template_name = 'common/list.html'  # to be overridden


class DetailView(generic.DetailView):
    exclude = ['id', ]


class CreateView(generic.CreateView):
    template_name = 'common/create.html'
    fields = []
    
    def form_valid(self, form):
        message_text = self.model.__name__ + ' is created.'
        messages.info(self.request, message_text)
        return super().form_valid(form)
    
    def get_success_url(self):
        return get_return_url(self.request)


class UpdateView(generic.UpdateView):
    template_name = 'common/update.html'
    fields = []
    
    def form_valid(self, form):
        message_text = self.model.__name__ + ' is updated.'
        messages.info(self.request, message_text)
        return super().form_valid(form)
    
    def get_success_url(self):
        return get_return_url(self.request)


class DeleteView(generic.DeleteView):
    template_name = 'common/delete.html'
    
    def delete(self, request, *args, **kwargs):
        message_text = self.model.__name__ + ' is deleted.'
        messages.info(self.request, message_text)
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return get_return_url(self.request)


#  expert classes ##################################################################################
class ExpertList(ListView):
    template_name = 'expert/expert_list.html'
    model = models.Expert


class CreateUpdateMixin:
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except URLError:
            messages.error(self.request, 'Expert object CANNOT be saved due to bad url!')
            return self.form_invalid(form)


class ExpertCreate(CreateUpdateMixin, CreateView):
    # todo: exclude self from choices of friends field
    model = models.Expert
    fields = ['name', 'long_url', 'friends', ]


class ExpertUpdate(CreateUpdateMixin, UpdateView):
    # todo: exclude self from choices of friends field
    model = models.Expert
    fields = ['name', 'long_url', 'friends', ]


class ExpertDelete(DeleteView):
    model = models.Expert


def expert_detail(request, pk):
    template_name = 'expert/expert_detail.html'
    
    if request.method == "GET":
        expert = models.Expert.objects.get(pk=pk)
        return render(request, template_name=template_name, context={'expert': expert})
    
    if request.method == "POST":
        expert = models.Expert.objects.get(pk=pk)
        term = request.POST.get('term')
        context = {
            'expert'     : expert,
            'term'       : term,
            'connections': expert.connections(term)
        }
        return render(request, template_name=template_name, context=context)
