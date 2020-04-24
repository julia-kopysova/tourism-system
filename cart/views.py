from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from polls.models import Type, Item
from .cart import Cart
from .forms import CartAddItemForm
import logging, logging.config
import sys
from datetime import datetime, timedelta

@require_POST
def cart_add(request, pk):
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

    type = get_object_or_404(Type, pk=pk)
    cart = Cart(request)
    form = CartAddItemForm(request.POST)
    logging.info('Outside')

    if form.is_valid():
        logging.info('Inside')
        logging.info(form)
        cd = form.cleaned_data
        logging.info(form)
        finish = cd['date_start'] + timedelta(days = type.days)
        item = Item(type_ticket = type, name_person = cd['name_person'], surname_person = cd['surname_person'], date_start = cd['date_start'], date_finish = finish)
        logging.info(item.type_ticket)
        logging.info(item.name_person)
        logging.info(item.surname_person)
        logging.info(item.date_start)
        item.save()
        cart.add(item)

    else:
        logging.info('Else')
        form = CartAddItemForm(request.POST)
    return redirect('account')

def cart_remove(request, pk):
    cart = Cart(request)
    item = get_object_or_404(Item, pk=pk)
    cart.remove(item)
    return redirect('account')
