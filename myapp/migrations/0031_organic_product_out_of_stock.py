# Generated by Django 4.2.14 on 2024-08-22 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_remove_billingdetail_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organic_product',
            name='out_of_stock',
            field=models.BooleanField(default=False),
        ),
    ]
