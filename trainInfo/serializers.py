from rest_framework import serializers
from .models import Booking, Train


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            "train_id",
            "train_name",
            "departure_station",
            "arrival_station",
            "departure_time",
            "arrival_time",
            "seats_available_count",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
