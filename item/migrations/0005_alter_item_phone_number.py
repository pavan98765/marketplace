# Generated by Django 4.2 on 2023-04-17 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_item_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
