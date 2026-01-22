from django import forms
from .models import Booking
from users.models import Profile


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["instructor", "date", "time_slot"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "w-full border rounded p-2"}),
            "time_slot": forms.Select(attrs={"class": "w-full border rounded p-2"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users with role="Instructor"

        self.fields['instructor'].queryset = Profile.objects.filter(role="instructor")
        self.fields['instructor'].empty_label = "Select an Instructor"