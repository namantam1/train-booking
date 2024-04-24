import random
import string
from typing import Any
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from trainInfo.models import Journey, Station, Train, Seat


class Command(BaseCommand):
    help = "Generate data for trains"

    def handle(self, *args, **options):
        Train.objects.all().delete()
        Station.objects.all().delete()
        self.create_mock_data()

    def create_mock_data(self, num_stations=5, num_trains=1, num_seats_per_journey=10):
        """Generate mock data for stations, trains, journeys, and seats."""
        # Create stations
        stations = [
            Station.objects.create(name=f"Station {i+1}") for i in range(num_stations)
        ]

        # Create trains
        for t in range(1, num_trains + 1):
            train_obj = Train.objects.create(train_name=f"Train {t}")

            hour = 1
            # Create journeys
            journeys = []
            for station_obj in stations:
                ref = timezone.datetime(year=2022, month=1, day=1, tzinfo=timezone.utc)
                arrival_time = ref + timezone.timedelta(hours=hour, minutes=0)
                departure_time = ref + timezone.timedelta(hours=hour, minutes=5)
                journey = Journey.objects.create(
                    train=train_obj,
                    station=station_obj,
                    arrival_time=arrival_time,
                    departure_time=departure_time,
                )
                journeys.append(journey)
                hour += 1

            # Create seats
            for journey in journeys:
                for i in range(num_seats_per_journey):
                    seat_number = f"S-{i+1}"
                    Seat.objects.create(
                        train=train_obj,
                        journey=journey,
                        seat_number=seat_number,
                    )

        print("Mock data generated successfully.")

    # def add_arguments(self, parser):
    #     pass
    #     # parser.add_argument("poll_ids", nargs="+", type=int)

    # def handle(self, *args, **options):
    #     Train.objects.all().delete()

    #     train = Train.objects.create(
    #         train_name="Express Train",
    #         departure_station="Station A",
    #         arrival_station="Station Z",
    #         departure_time=timezone.datetime(2024, 4, 20, 8, 0, tzinfo=timezone.utc),
    #         arrival_time=timezone.datetime(2024, 4, 20, 18, 0, tzinfo=timezone.utc),
    #     )
    #     self.stdout.write(self.style.SUCCESS("Train created: Express Train"))

    #     seats = [
    #         Seat(
    #             train=train,
    #             coach_number=chr(65 + i),
    #             seat_number=f"{chr(65 + i)}-{j:02}",
    #         )
    #         for i in range(3)
    #         for j in range(1, 101)
    #     ]
    #     Seat.objects.bulk_create(seats)

    #     self.stdout.write(
    #         self.style.SUCCESS(f"{len(seats)} Seats generated successfully!")
    #     )
