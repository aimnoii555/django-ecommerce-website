# Generated by Django 3.0 on 2021-11-26 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20211126_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpending',
            name='sliptime',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
