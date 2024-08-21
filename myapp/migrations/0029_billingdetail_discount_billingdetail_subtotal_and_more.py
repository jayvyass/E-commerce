# Generated by Django 4.2.14 on 2024-08-20 10:35

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_remove_billingdetail_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingdetail',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='billingdetail',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='billingdetail',
            name='total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
