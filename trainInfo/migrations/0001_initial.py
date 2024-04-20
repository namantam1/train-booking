# Generated by Django 4.2.11 on 2024-04-20 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('train_id', models.AutoField(primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=100)),
                ('departure_station', models.CharField(max_length=100)),
                ('arrival_station', models.CharField(max_length=100)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('seat_id', models.AutoField(primary_key=True, serialize=False)),
                ('coach_number', models.CharField(max_length=50)),
                ('seat_number', models.CharField(max_length=20)),
                ('is_booked', models.BooleanField(default=False)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainInfo.train')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=100)),
                ('booking_time', models.DateTimeField(auto_now_add=True)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainInfo.seat')),
            ],
        ),
    ]
