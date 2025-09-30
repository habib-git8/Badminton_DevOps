from django.contrib import admin
from .models import Court, Booking

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ("name", "location")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user_name", "court", "start_time", "end_time")
    list_filter = ("court", "start_time")
    search_fields = ("user_name",)
