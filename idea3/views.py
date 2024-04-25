from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import fetch_seats, book_seat as _book_seat, Stop, Train


@api_view(["GET"])
def get_trains(request):
    source = request.query_params.get("source")
    destination = request.query_params.get("destination")
    print(source, destination)
    data = fetch_seats(source, destination, cast=True)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_trains_routes(request):
    trains = Train.objects.all().prefetch_related("stop_set")[:10]
    data = [
        dict(
            train=train.name,
            seats_count=train.seats_count,
            stops=train.stop_set.order_by("arrival_time").values(
                "station__name", "arrival_time", "departure_time"
            ),
        )
        for train in trains
    ]
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_trains_routes_by_train(request):
    train = request.query_params.get("train")
    data = (
        Stop.objects.filter(train__name=train)
        .order_by("arrival_time")
        .values("train__name", "station__name", "arrival_time", "departure_time")
    )

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
def book_seat(request):
    source = request.data.get("source")
    destination = request.data.get("destination")
    train = request.data.get("train")
    data = _book_seat(train, source, destination)
    return Response(data={"status": data}, status=status.HTTP_201_CREATED)
