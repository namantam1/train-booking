from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from trainInfo.models import Train, Seat


class Command(BaseCommand):
    help = "Generate data for trains"

    def add_arguments(self, parser):
        parser.add_argument('-t', '--trains', type=int, default=1, help='Number of trains')
        parser.add_argument('-c', '--coaches', type=int, default=3, help='Number of coaches')
        parser.add_argument('-s', '--seats', type=int, default=100, help='Number of seats')


    def handle(self, *args, **options):
        Train.objects.all().delete()

        trains = options["trains"]
        coaches = options["coaches"]
        seats = options["seats"]

        for t in range(trains):
            train = Train.objects.create(
                train_name=f"Express Train {chr(65 + t)}",
                departure_station="Station A",
                arrival_station="Station Z",
                departure_time=timezone.datetime(2024, 4, 20, 8, 0, tzinfo=timezone.utc),
                arrival_time=timezone.datetime(2024, 4, 20, 18, 0, tzinfo=timezone.utc),
            )
            self.stdout.write(self.style.SUCCESS(f"Train created: {train.train_name}"))

            seat_objs = [
                Seat(
                    train=train,
                    coach_number=chr(65 + i),
                    seat_number=f"{chr(65 + i)}-{j:02}",
                )
                for i in range(coaches) # coached
                for j in range(1, seats+1) # seats
            ]
            Seat.objects.bulk_create(seat_objs)

            self.stdout.write(
                self.style.SUCCESS(f"{seats} Seats with {coaches} coaches generated successfully!")
            )
