# Generated by Django 2.2.6 on 2020-06-03 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='sight',
            name='minutes_needs',
            field=models.PositiveIntegerField(default=60),
        ),
        migrations.AddField(
            model_name='sight',
            name='normal_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
