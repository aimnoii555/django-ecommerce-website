# Generated by Django 3.0 on 2021-11-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_cart_stamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='stamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
