from django.contrib import admin

from trainInfo.models import Booking, Seat, Train

# Register your models here.
admin.site.register([Train, Seat])


@admin.register(Booking)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["admin_booking_time", "seat_number"]
    list_select_related = ["seat"]

    @admin.display(description="booking_time")
    def admin_booking_time(self, obj):
        return obj.booking_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
