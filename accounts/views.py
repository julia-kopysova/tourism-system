from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, EditAccountForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from polls.models import Type, Item, Review,Order
from cart.cart import Cart
from cart.forms import CartAddItemForm
from accounts.forms import  WriteReviewForm
from django.utils import timezone
from datetime import date
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

def write_review(response):
    if response.method == "POST":
        user = response.user
        form = WriteReviewForm(response.POST)
        if form.is_valid():
            logging.info(form)
            cd = form.cleaned_data
            review = Review( user = user, title = cd['title'], text = cd['text'], date_write = date.today())
            review.save()
            return redirect('prices')
    else:
        form = WriteReviewForm()
    return render(response, 'review.html', {'form': form})




def own_account(request):
    cart = Cart(request)
    user = request.user
    orders_filter = Order.objects.filter(user = user, paid = 'True')
    tickets = []
    try:
        logging.info(orders_filter)
        #ordersget = Order.objects.get(user = user, paid = 'True')
        for order in orders_filter:
            all_tickets_in_one_order = order.items.all()
            for one in all_tickets_in_one_order:
                logging.info(one.id)
                one_ticket = Item.objects.get(id = one.id)
                tickets.append(one_ticket)
    except Order.DoesNotExist:
        orders_filter = None
    logging.info(tickets)
    #logging.info(ordersget)
    return render(request,'account.html', {'cart': cart, 'tickets':tickets})

def signup(response):
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(response, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(response, 'signup.html', {'form': form})

def edit_account(response):
    if response.method == "POST":
        form = EditAccountForm(response.POST, instance=response.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/account')
    else:
        form = EditAccountForm(instance=response.user)
    return render(response, 'edit_account.html',{"form": form})

def change_password(response):
    if response.method == "POST":
        form = PasswordChangeForm(data=response.POST, user=response.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(response, form.user)
            return redirect('/accounts/account')
        else:
            return redirect('/accounts/account/change_password')
    else:
        form = PasswordChangeForm(user=response.user)
    return render(response, 'change_password.html',{"form": form})
