# Generated by Django 4.2.11 on 2024-04-23 11:54

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
                ('train_id', models.IntegerField(primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('stop_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField()),
                ('train_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='idea1.train')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('seat_id', models.IntegerField(primary_key=True, serialize=False)),
                ('seat_number', models.CharField(max_length=10)),
                ('is_booked', models.BooleanField(default=False)),
                ('stop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='idea1.stop')),
                ('train_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='idea1.train')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('destination_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_stop', to='idea1.stop')),
                ('seat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='idea1.seat')),
                ('source_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_stop', to='idea1.stop')),
                ('train_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='idea1.train')),
            ],
        ),
    ]