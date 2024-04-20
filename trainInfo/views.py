from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking, Train, Seat
from django.db import transaction
from .serializers import BookingSerializer, TrainSerializer


@api_view(["GET"])
def get_trains(request):
    trains = Train.objects.all()
    serializer = TrainSerializer(trains, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def book_seat(request):
    user_id = request.data.get("user_id")

    # Using atomic transaction to ensure that booking process is atomic
    with transaction.atomic():
        # Find an available seat
        seat = Seat.objects.select_for_update().filter(is_booked=False).first()
        if seat is None:
            return Response(
                {"error": "No seats available."}, status=status.HTTP_200_OK
            )

        # Create a booking for the available seat
        booking = Booking.objects.create(seat=seat, user_id=user_id)
        seat.is_booked = True
        seat.save()

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
