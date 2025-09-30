from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Court(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        # Ensure end time is after start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

        # Prevent overlapping bookings for same court
        overlapping = Booking.objects.filter(
            court=self.court,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("This court is already booked for that time.")

    def __str__(self):
        return f"{self.user_name} booked {self.court.name} ({self.start_time} - {self.end_time})"
