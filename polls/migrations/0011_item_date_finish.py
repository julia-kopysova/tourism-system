# Generated by Django 2.2.6 on 2020-04-24 08:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20200412_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date_finish',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
