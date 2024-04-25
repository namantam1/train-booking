# models.py

from django.db import models, transaction
from django.utils import timezone
from django.db.models import F, Q, OuterRef, Subquery, Count
from django.db.models.functions import Coalesce


class Train(models.Model):
    train_id = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=100)

    def __str__(self):
        return self.train_name


class Stop(models.Model):
    stop_id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100, db_index=True)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"{self.station_name} - {self.train}"


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"Seat {self.seat_number} - {self.train}"


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    journey_start_stop = models.ForeignKey(
        Stop, related_name="start_booking", on_delete=models.CASCADE
    )
    journey_end_stop = models.ForeignKey(
        Stop, related_name="end_booking", on_delete=models.CASCADE
    )
    booking_date = models.DateTimeField()

    def __str__(self):
        return f"Booking {self.booking_id} - {self.seat}"


def get_seats(source, destination):
    stops = (
        Stop.objects.filter(station_name__in=[source, destination])
        .order_by("arrival_time")
        .values_list("stop_id", flat=True)
    )

    trains_with_seats = Train.objects.annotate(
        total_seats=Count("seat"),
        booked_seats=Coalesce(
            Subquery(
                Booking.objects.filter(
                    Q(journey_start_stop__in=Subquery(stops))
                    | Q(journey_end_stop__in=Subquery(stops)),
                    ~Q(journey_end_stop__station_name=source),
                    seat__train=OuterRef("pk"),
                ).values("booking_id")
            ),
            0,
        ),
    ).annotate(available_seats=F("total_seats") - F("booked_seats"))
    return trains_with_seats


@transaction.atomic
def book_seat(train_id, source, destination):
    # Get the stops corresponding to the source and destination
    stops = Stop.objects.filter(station_name__in=[source, destination]).order_by(
        "arrival_time"
    )

    # Check if the stops exist
    if stops.count() != 2:
        return None  # Source or destination not found

    start_stop = stops.first()
    end_stop = stops.last()

    # Check if there's an available seat for the given train, source, and destination
    booked = Booking.objects.filter(
        Q(journey_start_stop__in=Subquery(stops))
        | Q(journey_end_stop__in=Subquery(stops)),
        ~Q(journey_end_stop__station_name=source),
        seat__train=train_id,
    ).exists()
    if not booked:
        booking = Booking.objects.create(
            seat=Seat.objects.first(),
            journey_start_stop=start_stop,
            journey_end_stop=end_stop,
            booking_data=timezone.now(),
        )
        return booking


def generate():
    Train.objects.all().delete()
    trains = [Train.objects.create(train_name=f"Train {t+1}") for t in range(1)]
    print(trains)

    for train in trains:
        ref = timezone.datetime(year=2022, month=1, day=1, tzinfo=timezone.utc)
        stops = [
            Stop.objects.create(
                train=train,
                station_name=f"Station {s+1}",
                arrival_time=ref + timezone.timedelta(hours=s + 1, minutes=0),
                departure_time=ref + timezone.timedelta(hours=s + 1, minutes=5),
            )
            for s in range(5)
        ]
        print(stops)
        seats = [
            Seat.objects.create(train=train, seat_number=f"S-{s+1:02}")
            for s in range(5)
        ]
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
