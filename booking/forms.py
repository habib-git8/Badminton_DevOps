from django import forms
from .models import Court, Booking

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ["name", "location"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["court", "user_name", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
