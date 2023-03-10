# Generated by Django 3.2.16 on 2023-01-29 11:14

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20230128_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='logo',
        ),
        migrations.CreateModel(
            name='CompanyLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=core.models.company_image_file_path)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.company')),
            ],
        ),
    ]
