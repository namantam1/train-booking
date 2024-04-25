from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import fetch_seats, book_seat as _book_seat


@api_view(["GET"])
def get_trains(request):
    source = request.query_params.get("source")
    destination = request.query_params.get("destination")
    print(source, destination)
    data = fetch_seats(source, destination, cast=True)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
def book_seat(request):
    source = request.data.get("source")
    destination = request.data.get("destination")
    train = request.data.get("train")
    data = _book_seat(train, source, destination)
    return Response(data={"status": data}, status=status.HTTP_201_CREATED)
