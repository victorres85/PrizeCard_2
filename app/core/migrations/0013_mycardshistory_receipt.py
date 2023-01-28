# Generated by Django 3.2.16 on 2023-01-26 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20230125_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_key', models.CharField(max_length=300, unique=True)),
                ('Shopper', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.shopper')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.card')),
            ],
        ),
        migrations.CreateModel(
            name='MyCardsHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=6)),
                ('finalized', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.card')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.company')),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shopper')),
            ],
        ),
    ]