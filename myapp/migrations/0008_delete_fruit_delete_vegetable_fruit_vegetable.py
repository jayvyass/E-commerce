# Generated by Django 4.2.14 on 2024-08-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_fruit_vegetable'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Fruit',
        ),
        migrations.DeleteModel(
            name='Vegetable',
        ),
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('fruit_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='fruits/images/')),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Vegetable',
            fields=[
                ('vegetable_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='vegetables/images/')),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
