from django import forms
from django.contrib.auth.models import User
from polls.models import Type, Item


class CartAddItemForm(forms.Form):
    name_person = forms.CharField(max_length=2000)
    surname_person = forms.CharField(max_length=2000)
    date_start = forms.CharField(max_length=2000)

    #date_start = forms.DateField(input_formats=['%m/%d/%Y %H:%M'])
