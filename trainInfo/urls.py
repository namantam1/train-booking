from django.urls import path

from trainInfo.views import get_trains

urlpatterns = [
    path("trains/", get_trains, name="get-trains"),
    # path("book-seat/", book_seat, name="book_seat"),
]
