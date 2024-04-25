from django.db import models
from django.db.models import *
from datetime import timedelta, datetime, timezone


# Create your models here.
class Train(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stop(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100, db_index=True)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"{self.station_name} - {self.train}"


class Seat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.train} - {self.number}"


def generate(
    trains=["Train 1", "Train 2"],
    stationss=(
        ["Station 1", "Station 2", "Station 3"],
        ["Station 1", "S-1", "Station 2", "Station 3"],
    ),
    hrs=[(1, 1), (6, 1)],
    seats_count=5,
):
    Train.objects.all().delete()

    for train_name, stations, hr in zip(trains, stationss, hrs):
        train = Train.objects.create(name=train_name)
        print(train)
        stops = []
        h, d = hr
        ref = datetime(2022, 1, 1, tzinfo=timezone.utc)
        for station in stations:
            stops.append(
                Stop(
                    train=train,
                    station_name=station,
                    arrival_time=ref + timedelta(hours=h, minutes=0),
                    departure_time=ref + timedelta(hours=h, minutes=5),
                )
            )
            h += d
        stops = Stop.objects.bulk_create(stops)
        print(stops)

        seats = [
            Seat(train=train, stop=stop, number=f"S-{s+1:02}")
            for stop in stops
            for s in range(seats_count)
        ]
        seats = Seat.objects.bulk_create(seats)
        print(seats)


def fetch(source="Station 1", destination="Station 3"):
    # Get all stops where the station name matches either the source or destination
    source_stops = Stop.objects.filter(station_name=source)
    destination_stops = Stop.objects.filter(station_name=destination)

    # Get subqueries for the arrival times of the source and destination stops
    source_arrival_time = Subquery(
        source_stops.filter(train=OuterRef("pk")).values("arrival_time")[:1]
    )
    destination_arrival_time = Subquery(
        destination_stops.filter(train=OuterRef("pk")).values("arrival_time")[:1]
    )
    # seats = Subquery(
    #     Seat.objects.filter(train=OuterRef("pk"), is_booked=False).values("pk")
    # )

    # Filter trains based on stops matching the source and destination
    # Ensure the order of stops is maintained by comparing arrival times
    trains = (
        Train.objects.filter(stop__in=source_stops)
        .filter(stop__in=destination_stops)
        .annotate(
            source_arrival_time=source_arrival_time,
            destination_arrival_time=destination_arrival_time,
        )
        .annotate(count=Count("seats"))
        .filter(source_arrival_time__lt=destination_arrival_time)
    )

    return trains
