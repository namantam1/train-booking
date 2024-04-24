from django.contrib import admin
from .models import Train, Seat, Booking

admin.site.register([Train, Seat, Booking])


# @admin.register(Booking)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ["admin_booking_time", "seat_number"]
#     list_select_related = ["seat"]

#     @admin.display(description="booking_time")
#     def admin_booking_time(self, obj):
#         return obj.booking_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
