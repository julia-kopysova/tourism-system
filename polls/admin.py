from django.contrib import admin
from .models import Sight, Type, Item, Review, Order
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'paid']
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'date_write', 'text']

admin.site.register(Sight)
admin.site.register(Type)
admin.site.register(Item)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Order, OrderAdmin)
