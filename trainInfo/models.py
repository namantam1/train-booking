from django.db import models


class Train(models.Model):
    train_id = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=100)
    departure_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    @property
    def seats_available_count(self):
        return Seat.objects.filter(train=self, is_booked=False).count


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    coach_number = models.CharField(max_length=50)
    seat_number = models.CharField(max_length=20)
    is_booked = models.BooleanField(default=False)


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    booking_time = models.DateTimeField(auto_now_add=True)

    @property
    def seat_number(self):
        return self.seat.seat_number

    @property
    def coach_number(self):
        return self.seat.coach_number
