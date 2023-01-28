# Generated by Django 3.2.16 on 2023-01-19 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_card_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('address2', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('region', models.CharField(blank=True, max_length=50)),
                ('post_code', models.CharField(max_length=10)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('lat', models.CharField(blank=True, max_length=20, null=True)),
                ('long', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]