from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from polls.models import Type, Item
from .cart import Cart
from .forms import CartAddItemForm

@require_POST
def cart_add(request, pk):
    type = get_object_or_404(Type, pk=pk)
    cart = Cart(request)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        form.save()
        cd = form.cleaned_data
        item = Item(type_tiket = type, name_person = cd['name_person'], surname_person = cd['surname_person'], date_start = cd['date_start'])
        item.save()
        cart.add(item)
    else:
        form = CartAddItemForm(request.POST)
    return redirect('account')
