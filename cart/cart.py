from decimal import Decimal
from django.conf import settings
from polls.models import Type, Item
from .forms import CartAddItemForm
import logging, logging.config
import sys

class Cart(object):
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

    def __init__(self, request):
        #Initialize the cart.
        logging.info('Initialize')
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        logging.info(cart)
        if not cart:
            logging.info('In if')
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item):
        item_id = str(item.id)
        self.cart[item_id] = { 'id': str(item.id),
                              'price': str(item.type_ticket.price),
                              'days':str(item.type_ticket.days),
                              'type':str(item.type_ticket.type),
                              #'price': str(item.type_ticket.price),
                              'name_person':str(item.name_person),
                              'surname_person': str(item.surname_person),
                              'date_start': str(item.date_start)}
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()
    def __iter__(self):
        # Объект, который будет возвращать данные, по одному элементу за раз.
        #The __iter__() method returns the iterator object itself.
        item_ids = self.cart.keys()
        # get the product objects and add them to the cart
        items = Item.objects.filter(id__in=item_ids)
        for item in items:
            self.cart[str(item.id)]['item'] = item
        for i in self.cart.values(): #значения в словаре
            i['price'] = Decimal(i['price'])
            yield i #вернeт генератор
    def get_total_price(self):
        return sum(Decimal(i['price'])  for i in self.cart.values())
    def clear(self):
    # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
