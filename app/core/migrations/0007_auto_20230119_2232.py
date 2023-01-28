# Generated by Django 3.2.16 on 2023-01-19 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_company_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='business_name',
        ),
        migrations.AddField(
            model_name='card',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.company'),
            preserve_default=False,
        ),
    ]
