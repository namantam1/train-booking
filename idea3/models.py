from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import *
from datetime import timedelta, datetime, timezone


class ArrayAppend(Func):

    function = "array_append"
    template = "%(function)s(%(expressions)s, %(element)s)"
    arity = 1

    def __init__(self, expression: str, element, **extra):
        if not isinstance(element, (str, int)):
            raise TypeError(
                f'Type of "{element}" must be int or str, '
                f'not "{type(element).__name__}".'
            )

        super().__init__(
            expression,
            element=isinstance(element, int) and element or f"'{element}'",
            **extra,
        )


# Create your models here.
class Train(models.Model):
    name = models.CharField(max_length=100)
    seats_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Stop(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100, db_index=True)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    seats_booked = ArrayField(models.IntegerField(), default=list)

    def __str__(self):
        return f"{self.station_name} - {self.train}"


def generate(
    trains=["Train 1", "Train 2"],
    stationss=(
        ["Station 1", "Station 2", "Station 3"],
        ["Station 1", "S-1", "Station 2", "Station 3"],
    ),
    hrs=[(1, 1), (6, 1)],
    seats_count=[5, 5],
):
    Train.objects.all().delete()

    for train_name, stations, hr, seats in zip(trains, stationss, hrs, seats_count):
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
                    seats_count=seats,
                    arrival_time=ref + timedelta(hours=h, minutes=0),
                    departure_time=ref + timedelta(hours=h, minutes=5),
                )
            )
            h += d
        stops = Stop.objects.bulk_create(stops)
        print(stops)


def fetch_trains(source="Station 1", destination="Station 3"):
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

    # Filter trains based on stops matching the source and destination
    # Ensure the order of stops is maintained by comparing arrival times
    trains = (
        Train.objects.filter(stop__in=source_stops)
        .filter(stop__in=destination_stops)
        .annotate(
            source_arrival_time=source_arrival_time,
            destination_arrival_time=destination_arrival_time,
        )
        .filter(source_arrival_time__lt=destination_arrival_time)
    )

    return trains


def fetch_seats_for_train(train="Train 1", source="Station 1", destination="Station 3"):
    source = Stop.objects.get(station_name=source, train__name=train)
    destination = Stop.objects.get(station_name=destination, train__name=train)

    return (
        Stop.objects.filter(train__name=train)
        .filter(
            arrival_time__gte=source.arrival_time,
            arrival_time__lte=destination.arrival_time,
        )
        .aggregate(max_len=Max("seats_booked__len"))
    )


def fetch_seats(source="Station 1", destination="Station 3", cast=False):
    source_stops = Stop.objects.filter(station_name=source)
    destination_stops = Stop.objects.filter(station_name=destination)

    source_arrival_time = Subquery(
        source_stops.filter(train=OuterRef("pk")).values("arrival_time")[:1]
    )
    destination_arrival_time = Subquery(
        destination_stops.filter(train=OuterRef("pk")).values("arrival_time")[:1]
    )

    trains = (
        Train.objects.filter(stop__in=source_stops)
        .filter(stop__in=destination_stops)
        .annotate(
            source_arrival_time=source_arrival_time,
            destination_arrival_time=destination_arrival_time,
        )
        .annotate(
            seats_booked_count=Subquery(
                Stop.objects.filter(
                    train=OuterRef("pk"),
                    arrival_time__gte=OuterRef("source_arrival_time"),
                    arrival_time__lte=OuterRef("destination_arrival_time"),
                )
                .order_by("-seats_booked__len")
                .values("seats_booked__len")[:1]
            ),
        )
        .filter(source_arrival_time__lt=destination_arrival_time)
    )

    if cast:
        return trains.values(
            "id",
            "name",
            "source_arrival_time",
            "destination_arrival_time",
            "seats_booked_count",
            "seats_count",
        )

    return trains


def book_seat(train="Train 1", source="Station 1", destination="Station 3"):
    train = Train.objects.get(name=train)
    source_stop = Stop.objects.get(station_name=source, train=train)
    destination_stop = Stop.objects.get(station_name=destination, train=train)
    stops = Stop.objects.filter(
        train=train,
        arrival_time__gte=source_stop.arrival_time,
        arrival_time__lte=destination_stop.arrival_time,
    )
    seats_booked = stops.values_list("seats_booked", flat=True)
    seats_booked = map(set, seats_booked)
    seats = set(range(1, train.seats_count + 1))
    for seat_booked in seats_booked:
        seats -= seat_booked

    if len(seats) != 0:
        seat = seats.pop()
        return stops.update(seats_booked=ArrayAppend("seats_booked", seat))
