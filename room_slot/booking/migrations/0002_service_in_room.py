# Generated by Django 3.0.3 on 2021-04-07 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_auto_20210407_1128'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service_in_room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_dtno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Booking_detail')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.Service')),
            ],
            options={
                'unique_together': {('book_dtno', 'sid')},
            },
        ),
    ]
