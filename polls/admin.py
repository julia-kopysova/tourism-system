from django.contrib import admin
from .models import Sight, Type, Item, Review
# Register your models here.
admin.site.register(Sight)
admin.site.register(Type)
admin.site.register(Item)
admin.site.register(Review)
