from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import get_seats, Booking


@api_view(["GET"])
def get_trains(request):
    source_id = request.query_params.get("source_id")
    destination_id = request.query_params.get("destination_id")
    print(source_id, destination_id)
    data = []
    for el in get_seats(source_id, destination_id):
        data.append(
            dict(
                train_name=el.train_name,
                total_seats=el.total_seats,
                booked_seats=el.booked_seats,
                available_seats=el.available_seats,
            )
        )
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
def book_seat(request):
    source = request.data.get("source")
    destination = request.data.get("destination")
    train = request.data.get("train")

    Booking.objects.create()
