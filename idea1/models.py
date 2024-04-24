from django.db import models
from django.utils import timezone


class Train(models.Model):
    train_name = models.CharField(max_length=100)


class Stop(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()


class Seat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)


class Booking(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    source_stop = models.ForeignKey(
        Stop, related_name="source_stop", on_delete=models.CASCADE
    )
    destination_stop = models.ForeignKey(
        Stop, related_name="destination_stop", on_delete=models.CASCADE
    )
    user_id = models.IntegerField()


def generate():
    Train.objects.all().delete()
    trains = [Train.objects.create(train_name=f"t-{t+1}") for t in range(1)]
    print(trains)
    for train in trains:
        ref = timezone.datetime(year=2022, month=1, day=1, tzinfo=timezone.utc)
        stops = [
            Stop.objects.create(
                train=train,
                name=f"sp-{s+1}",
                arrival_time=ref + timezone.timedelta(hours=s + 1, minutes=0),
                departure_time=ref + timezone.timedelta(hours=s + 1, minutes=5),
            )
            for s in range(5)
        ]

        st = 1
        print(stops)
        for stop in stops:
            seat = Seat.objects.create(train=train, stop=stop, seat_number=f"st-{st}")
            st += 1
            print(seat)


from django.db.models import Subquery, OuterRef


def get_trains(source, destination):
    Train.objects.all().annotate(
        seats=Subquery(
            Stop.objects.filter(
                id=OuterRef("pk"),
            )
        )
    )
