# Generated by Django 3.0 on 2021-11-26 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20211126_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpending',
            name='other',
            field=models.TextField(blank=True, null=True),
        ),
    ]
