# Generated by Django 5.0.4 on 2024-04-30 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_product_piece'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='composition',
        ),
    ]
