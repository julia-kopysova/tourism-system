from django.urls import path
from . import views as v
from django.views.generic.base import TemplateView
from django.conf import settings
from cart import views as views_cart
from checkout import views as views_checkout

urlpatterns = [
    path('', v.HomeView.as_view(), name='home'),
    path('sight/<slug>/', v.SightDatailView.as_view(), name ='sight'),
    path('howitworks/', TemplateView.as_view(template_name='howitworks.html'), name='howitworks'),
    path('prices/', v.PricesView.as_view(), name='prices'),
    path('ticket/<pk>/', v.PricesDetail.as_view(), name='ticket'),
    path('add/<pk>', views_cart.cart_add, name='add'),
    path('checkout/', views_checkout.checkout, name='checkout'),
    path('process-payment/', views_checkout.process_payment, name='process_payment'),
    path('payment-done/', views_checkout.payment_done, name='payment_done'),
    path('payment-cancelled/', views_checkout.payment_canceled, name='payment_cancelled'),
    path('remove/<pk>', views_cart.cart_remove, name='remove'),
    path('guidebook/', v.GuidebookView.as_view(), name='guidebook'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
]
