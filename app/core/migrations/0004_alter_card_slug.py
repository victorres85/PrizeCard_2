# Generated by Django 3.2.16 on 2023-01-18 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_card_business_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]
