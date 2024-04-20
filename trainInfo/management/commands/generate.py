from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from trainInfo.models import Train, Seat


class Command(BaseCommand):
    help = "Generate data for trains"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        Train.objects.all().delete()

        train = Train.objects.create(
            train_name="Express Train",
            departure_station="Station A",
            arrival_station="Station Z",
            departure_time=timezone.datetime(2024, 4, 20, 8, 0, tzinfo=timezone.utc),
            arrival_time=timezone.datetime(2024, 4, 20, 18, 0, tzinfo=timezone.utc),
        )
        self.stdout.write(self.style.SUCCESS("Train created: Express Train"))

        seats = [
            Seat(
                train=train,
                coach_number=chr(65 + i),
                seat_number=f"{chr(65 + i)}-{j:02}",
            )
            for i in range(3)
            for j in range(1, 101)
        ]
        Seat.objects.bulk_create(seats)

        self.stdout.write(
            self.style.SUCCESS(f"{len(seats)} Seats generated successfully!")
        )
