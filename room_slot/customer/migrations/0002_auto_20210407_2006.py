# Generated by Django 3.0.3 on 2021-04-07 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='mid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Member'),
        ),
    ]
