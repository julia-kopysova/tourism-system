from django.contrib import admin
from .models import Sight, Type, Item, Review, Order,Profile, Feedback, Questions
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'paid']
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'date_write', 'text']
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','message','date']
    search_fields = ['name', 'email']
    date_hierarchy = 'date'


admin.site.register(Sight)
admin.site.register(Questions)
admin.site.register(Profile)
admin.site.register(Type)
admin.site.register(Item)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
