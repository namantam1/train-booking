from django.urls import path

# from trainInfo.views import get_trains
from idea3.views import (
    get_trains,
    book_seat,
    get_trains_routes,
    get_trains_routes_by_train,
)

urlpatterns = [
    path("trains/", get_trains, name="get-trains"),
    path("routes/", get_trains_routes, name="routes"),
    path("routes/train/", get_trains_routes_by_train, name="train-routes"),
    path("book-seat/", book_seat, name="book_seat"),
]
