from django.urls import path
from .views import book_seat, get_trains

urlpatterns = [
    path("trains/", get_trains, name="train-list"),
    path("book-seat/", book_seat, name="book-seat"),
]
