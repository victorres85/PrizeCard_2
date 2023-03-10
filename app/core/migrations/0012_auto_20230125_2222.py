# Generated by Django 3.2.16 on 2023-01-25 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_shooper_mycards_shopper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycards',
            name='card',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.card'),
        ),
        migrations.AlterField(
            model_name='mycards',
            name='shopper',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.shopper'),
        ),
    ]
