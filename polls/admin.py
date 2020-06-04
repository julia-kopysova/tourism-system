from typing import Set
from django.contrib import admin
from .models import Sight, Type, Item, Review, Order, Profile, Feedback, Questions
# Register your models here.


class ItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_person', 'surname_person', 'visited_times','date_start','date_finish', 'paid']
    search_fields = ['id']
    date_hierarchy = 'date_start'
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]
        if not is_superuser:
            disabled_fields |= {
                'id',
                'type',
                'name_person',
                'surname_person',
                'date_start',
                'date_finish',
                'paid',
            }
        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'id',
                'type'
                'name_person',
                'surname_person',
                'date_start',
                'date_finish',
                'paid',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date', 'paid']
    list_filter = ['id']

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'field']
    list_filter = ['field']

class SightAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_sight', 'slug']
    list_filter = ['id']
    search_fields = ['name_sight']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'date_write', 'text']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','message','date']
    search_fields = ['name', 'email']
    date_hierarchy = 'date'

class TypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'days', 'price']
    search_fields = ['id']


admin.site.register(Sight,SightAdmin)
admin.site.register(Profile)
admin.site.register(Type,TypeAdmin)
admin.site.register(Questions,QuestionsAdmin)
admin.site.register(Item,ItemsAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
