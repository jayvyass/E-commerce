# Generated by Django 4.2.14 on 2024-08-20 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_billingdetail_discount_billingdetail_subtotal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingdetail',
            name='amount',
        ),
        migrations.AlterField(
            model_name='billingdetail',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
