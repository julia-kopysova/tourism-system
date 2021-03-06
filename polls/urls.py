from django.urls import path
from . import views as v
from django.views.generic.base import TemplateView
from django.conf import settings
from cart import views as views_cart
from checkout import views as views_checkout
from accounts import views as v_a

urlpatterns = [
    path('', v.HomeView.as_view(), name='home'),
    path('sight/<slug>/', v.SightDatailView.as_view(), name ='sight'),
    path('howitworks/', v.Howitworks.as_view(), name='howitworks'),
    path('prices/', v.PricesView.as_view(), name='prices'),
    path('ticket/<pk>/', v.PricesDetail.as_view(), name='ticket'),
    path('add/<pk>', views_cart.cart_add, name='add'),
    path('checkout/', views_checkout.checkout, name='checkout'),
    path('process-payment/', views_checkout.process_payment, name='process_payment'),
    path('payment-done/', views_checkout.payment_done, name='payment_done'),
    path('payment-cancelled/', views_checkout.payment_canceled, name='payment_cancelled'),
    path('remove/<pk>', views_cart.cart_remove, name='remove'),
    path('delete_all/', views_cart.delete_all_cart, name='delete_all'),
    path('guidebook/', v.GuidebookView.as_view(), name='guidebook'),
    path('cart/', v_a.cart_display, name='cart'),
    path('faq/', v.feedback, name='faq'),
]
