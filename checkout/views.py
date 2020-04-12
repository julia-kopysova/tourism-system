from django.shortcuts import render
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from cart.cart import Cart
from polls.models import Type, Item, Order
# Create your views here.
def checkout(request):
    user = request.user
    cart = Cart(request)
    o = Order(
                user = user,
            )
    o.save()
    for i in cart:
        one = Item.objects.get(id = i['id'])
        o.items.add(one)
    cart.clear()
    return render(request,'checkout.html', {'cart': cart})
