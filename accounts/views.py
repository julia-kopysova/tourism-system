from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, EditAccountForm, EditProfileForm, ProfileForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from polls.models import Type, Item, Review,Order, Profile
from cart.cart import Cart
from cart.forms import CartAddItemForm
from accounts.forms import  WriteReviewForm
from django.utils import timezone
import datetime
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

def cart_display(request):
    cart = Cart(request)
    return render(request,'basket.html', {'cart': cart})



def own_account(request):
    cart = Cart(request)
    user = request.user
    orders_filter = Order.objects.filter(user = user, paid = 'True')
    d1 = datetime.datetime.now()
    d2 = datetime.datetime(user.date_joined.year,user.date_joined.month,user.date_joined.day,user.date_joined.hour,user.date_joined.minute,user.date_joined.second)
    days_in_system = (d1 - d2).days
    #days_in_system = (timezone.now - user.date_joined).days
    tickets_active = []
    ticket_history = []
    #now = datetime.date.now()
    try:
        logging.info(orders_filter)
        #ordersget = Order.objects.get(user = user, paid = 'True')
        for order in orders_filter:
            all_tickets_in_one_order = order.items.all()
            for one in all_tickets_in_one_order:
                logging.info(one.id)
                one_ticket = Item.objects.get(id = one.id)
                if d1 > datetime.datetime(one_ticket.date_finish.year,one_ticket.date_finish.month,one_ticket.date_finish.day) :
                    ticket_history.append(one_ticket)
                else:
                    tickets_active.append(one_ticket)
    except Order.DoesNotExist:
        orders_filter = None
    if not ticket_history:
        ticket_history = -1
        count = len(tickets_active)
    else:
        count = len(ticket_history)+ len(tickets_active)
    #logging.info(tickets)
    #logging.info(ordersget)
    return render(request,'account.html', {'cart': cart, 'tickets':tickets_active, 'ticket_history': ticket_history, 'count_cards':count, 'days_in_system':days_in_system})

def signup(response):
    if response.method == "POST":
        form = SignUpForm(response.POST)
        logging.info(form)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.gender = form.cleaned_data.get('gender')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(response, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(response, 'signup.html', {'form': form})

def edit_account(response):
    if response.method == "POST":
        form = EditAccountForm(response.POST, instance=response.user)
        profile_form = EditProfileForm(response.POST, instance=response.user.profile)
        logging.info(form)
        logging.info(profile_form)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('/accounts/account')
    else:
        form = EditAccountForm(instance=response.user)
        profile_form = EditProfileForm(instance=response.user.profile)
    return render(response, 'edit_account.html',{"form": form, "profile_form": profile_form})

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
