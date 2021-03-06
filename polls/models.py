from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Count
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class Sight(models.Model):
    name_sight = models.CharField(max_length=60)
    description = models.TextField()
    img = models.ImageField(upload_to='photo_sight')
    year = models.IntegerField()
    address = models.CharField(max_length=100)
    link = models.URLField()
    slug = models.SlugField()
    minutes_needs = models.PositiveIntegerField(default=60)
    normal_price = models.PositiveIntegerField(default=0)
    def get_absolute_url(self):
        return reverse("sight", kwargs = {
        'slug': self.slug
        })

TYPE_CHOICES = (
    ('VIP', 'VIP'),
    ('Lite', 'Lite')
)


class Questions(models.Model):
    FIELD_CHOICES = (
        ('Identification', 'Identification'),
        ('Transport', 'Transport'),
        ('Money', 'Money'),
        ('Attraction', 'Attraction'),
    )
    question = models.CharField(max_length=100)
    answer =  models.CharField(max_length=500)
    field = models.CharField(choices=FIELD_CHOICES, max_length=14)

class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Feedback"
    def __str__(self):
        return self.name + "-" +  self.email

class Type(models.Model):
    #type - lite or VIP
    type = models.CharField(choices=TYPE_CHOICES, max_length=4)
    days = models.IntegerField()
    desc = models.TextField()
    price = models.FloatField()
    type_slug = models.SlugField()
    def get_absolute_url(self):
        return reverse("ticket", kwargs = {
        'pk': self.id
        })

class Item(models.Model):
    type_ticket = models.ForeignKey(Type,on_delete=models.CASCADE)
    name_person = models.CharField(max_length=20)
    surname_person = models.CharField(max_length=20)
    date_start = models.DateField()
    date_finish = models.DateField(blank=True)
    visited_times = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=False)

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=200)
    date_write = models.DateField()
    class Meta:
         ordering = ['-date_write']

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    def total_cost(self):
        return Decimal(sum([ i.type_ticket.price for i in self.items.all() ] ))

class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
