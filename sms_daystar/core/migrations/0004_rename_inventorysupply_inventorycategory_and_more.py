# Generated by Django 5.0.4 on 2024-05-08 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_attendance_unique_together'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InventorySupply',
            new_name='InventoryCategory',
        ),
        migrations.RemoveField(
            model_name='inventorysupplyreceipt',
            name='supply',
        ),
    ]