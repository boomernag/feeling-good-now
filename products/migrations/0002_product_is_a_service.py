# Generated by Django 3.1.4 on 2020-12-15 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_a_service',
            field=models.BooleanField(default=False),
        ),
    ]
