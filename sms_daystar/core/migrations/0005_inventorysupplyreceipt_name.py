# Generated by Django 5.0.4 on 2024-05-08 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_inventorysupply_inventorycategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorysupplyreceipt',
            name='name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]