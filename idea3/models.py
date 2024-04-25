from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import *
from datetime import timedelta, datetime, timezone
from random import randint, sample


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
    name = models.CharField(max_length=100, db_index=True)
    seats_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self) -> str:
        return self.name


class Stop(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField(db_index=True)
    departure_time = models.DateTimeField()
    seats_booked = ArrayField(models.IntegerField(), default=list)

    def __str__(self):
        return f"{self.station} - {self.train}"


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
    Station.objects.all().delete()

    trains = Train.objects.bulk_create(
        [
            Train(name=name, seats_count=count)
            for name, count in zip(trains, seats_count)
        ]
    )
    print("Trains=", len(trains))

    for train, stations, hr in zip(trains, stationss, hrs):
        stations = Station.objects.bulk_create(
            [Station(name=name) for name in stations]
        )
        print(stations)

        ref = datetime(2022, 1, 1, tzinfo=timezone.utc)
        stops = []
        h, d = hr
        for station in stations:
            stops.append(
                Stop(
                    train=train,
                    station=station,
                    arrival_time=ref + timedelta(hours=h, minutes=0),
                    departure_time=ref + timedelta(hours=h, minutes=5),
                )
            )
            h += d
        stops = Stop.objects.bulk_create(stops)
        print(stops)


def fetch_seats(source="Station 1", destination="Station 3", cast=False):
    source_stops = Stop.objects.filter(station__name=source)
    destination_stops = Stop.objects.filter(station__name=destination)

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
    source_stop = Stop.objects.get(station__name=source, train=train)
    destination_stop = Stop.objects.get(station__name=destination, train=train)
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


def fetch_seats_for_train(train="Train 1", source="Station 1", destination="Station 3"):
    source = Stop.objects.get(station__name=source, train__name=train)
    destination = Stop.objects.get(station__name=destination, train__name=train)

    return (
        Stop.objects.filter(train__name=train)
        .filter(
            arrival_time__gte=source.arrival_time,
            arrival_time__lte=destination.arrival_time,
        )
        .aggregate(max_len=Max("seats_booked__len"))
    )


def select_elements_with_priority(lst, total, prioritized_indices, prior_selection):
    # Select n - len(prioritized_indices) random elements
    random_indices = [i for i in range(len(lst)) if i not in prioritized_indices]
    random_selection = sample(random_indices, total - prior_selection)
    random_prioritized_indices = sample(prioritized_indices, prior_selection)
    indices = sorted(random_selection + random_prioritized_indices)
    return [lst[i] for i in indices]


def generate_bulk_data():
    stations_count = 5000
    train_count = 15000
    seats_count = 2000

    min_stop_count = 20
    max_stops_count = 30

    trains_name = [f"Train {i+1}" for i in range(train_count)]
    stations_name = [f"Station {i+1}" for i in range(stations_count)]

    hrs = [(i, i + 1) for i in range(train_count)]

    Train.objects.all().delete()
    Station.objects.all().delete()

    trains = Train.objects.bulk_create(
        [Train(name=name, seats_count=seats_count) for name in trains_name]
    )
    print("Trains=", len(trains))

    stations = Station.objects.bulk_create(
        [Station(name=name) for name in stations_name]
    )
    print("Stations=", len(stations))

    stops = []
    for train, hr in zip(trains, hrs):
        h, d = hr
        ref = datetime(2022, 1, 1, tzinfo=timezone.utc)
        stops_count = randint(min_stop_count, max_stops_count)

        # stop_stations = sample(stations, stops_count)
        # indices = sample(range(len(stations)), stops_count)
        # stop_stations = [stations[i] for i in sorted(indices)]
        stop_stations = select_elements_with_priority(
            stations, stops_count, list(range(0, stations_count, 500)), 10
        )

        for station in stop_stations:
            stops.append(
                Stop(
                    train=train,
                    station=station,
                    arrival_time=ref + timedelta(hours=h, minutes=0),
                    departure_time=ref + timedelta(hours=h, minutes=5),
                )
            )
            h += d

    stops = Stop.objects.bulk_create(stops, 10000)
    print("Stops=", len(stops))
