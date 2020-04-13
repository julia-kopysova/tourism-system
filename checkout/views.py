from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from cart.cart import Cart
from polls.models import Type, Item, Order
from django.views.decorators.csrf import csrf_exempt
import logging, logging.config
import sys
# Create your views here.
def checkout(request):
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
    logging.info(o.id)
    logging.info(o.total_cost())
    request.session['order_id'] = o.id
    logging.info(request.session['order_id'])
    return redirect('process_payment')
    #return render(request,'checkout.html', {'cart': cart})

def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')
