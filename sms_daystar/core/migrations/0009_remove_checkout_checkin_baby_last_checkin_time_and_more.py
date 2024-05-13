# Generated by Django 5.0.4 on 2024-05-09 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_checkin_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='checkin',
        ),
        migrations.AddField(
            model_name='baby',
            name='last_checkin_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='baby',
            name='last_checkout_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='CheckIn',
        ),
        migrations.DeleteModel(
            name='CheckOut',
        ),
    ]