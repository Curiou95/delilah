# Generated by Django 5.0.4 on 2024-05-20 10:22

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_sitter_is_on_duty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitter',
            name='s_location',
            field=models.CharField(choices=[('kabalagala', 'KABALAGALA')], max_length=50),
        ),
        migrations.AlterField(
            model_name='sitter',
            name='s_tel',
            field=models.IntegerField(validators=[core.models.validate_numbers]),
        ),
    ]