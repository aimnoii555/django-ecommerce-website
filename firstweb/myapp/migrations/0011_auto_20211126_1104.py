# Generated by Django 3.0 on 2021-11-26 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_orderlist_orderpending'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpending',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
