from django.shortcuts import render, redirect, get_object_or_404
from .models import Sight, Type, Item, Review
from django.views.generic import ListView,DetailView
from cart.forms import CartAddItemForm
from django import forms
from django.views.generic.edit import FormMixin
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import FeedbackForm
import logging, logging.config
import sys
LOGGING = {
'version': 1,
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'stream': sys.stdout,
    }
},
'root': {
    'handlers': ['console'],
    'level': 'INFO'
}
}
logging.config.dictConfig(LOGGING)

class HomeView(ListView):
    model = Sight
    template_name = "home.html"

class SightDatailView(DetailView):
    model = Sight
    template_name = "sight_one.html"


class PricesView(ListView):
    model = Type
    template_name = "prices.html"
    context_object_name = 'types_list'
    queryset = Type.objects.all()
    def get_context_data(self, **kwargs):
        context = super(PricesView, self).get_context_data(**kwargs)
        context['list_vip'] = Type.objects.filter(type = 'VIP')
        context['list_lite'] = Type.objects.filter(type = 'Lite')
        context['reviews_list'] = Review.objects.all()
        context['count'] = len(Review.objects.all())
        return context

class PricesDatailView(DetailView):
    model = Type
    template_name = "detail.html"

class GuidebookView(ListView):
    model = Sight
    template_name = "sight_list.html"

class Howitworks(ListView):
    model = Review
    template_name = "howitworks.html"
    def get_context_data(self, **kwargs):
        context = super(Howitworks, self).get_context_data(**kwargs)
        context['count'] = len(Review.objects.all())
        return context


class PricesDetail(FormMixin, DetailView):
    model = Type
    form_class = CartAddItemForm
    template_name = "detail.html"
    def get_context_data(self, **kwargs):
        context  = super(PricesDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    def get_initial(self):
        return ({'ticket': self.get_object()})
    def get_success_url(self):
        return reverse('ticket', kwargs={'pk': self.object.id})
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sorry, you're not registered")
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        def form_valid(self, form):
        # pass message
            return super(PricesDetail, self).form_valid(form)


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        logging.info(form)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('faq')
    else:
        form = FeedbackForm()
    return render(request, 'faq.html', {'form': form})
