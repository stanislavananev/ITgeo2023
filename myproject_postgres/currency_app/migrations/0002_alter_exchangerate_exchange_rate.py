# Generated by Django 4.2.6 on 2023-10-15 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerate',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=6, max_digits=15),
        ),
    ]