from django.shortcuts import render, redirect, get_object_or_404
from .models import Sight, Type, Item
from django.views.generic import ListView,DetailView
from cart.forms import CartAddItemForm
from django import forms
from django.views.generic.edit import FormMixin
from django.http import HttpResponseForbidden

class HomeView(ListView):
    model = Sight
    template_name = "home.html"

class SightDatailView(DetailView):
    model = Sight
    template_name = "sight_one.html"

class PricesView(ListView):
    model = Type
    template_name = "prices.html"

class PricesDatailView(DetailView):
    model = Type
    template_name = "detail.html"

class GuidebookView(ListView):
    model = Sight
    template_name = "sight_list.html"

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
