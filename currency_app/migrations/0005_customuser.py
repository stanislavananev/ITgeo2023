# Generated by Django 4.2.6 on 2023-12-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_app', '0004_delete_exchangerate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
