from django.urls import path
from . import views as v
from django.views.generic.base import TemplateView
from django.conf import settings
from cart import views as views_cart

urlpatterns = [
    path('', v.HomeView.as_view(), name='home'),
    path('sight/<slug>/', v.SightDatailView.as_view(), name ='sight'),
    path('howitworks/', TemplateView.as_view(template_name='howitworks.html'), name='howitworks'),
    path('prices/', v.PricesView.as_view(), name='prices'),
    path('ticket/<pk>/', v.PricesDetail.as_view(), name='ticket'),
    path('add/<pk>', views_cart.cart_add, name='add'),
    path('remove/<pk>', views_cart.cart_remove, name='remove'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
]
