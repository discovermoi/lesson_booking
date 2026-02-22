from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Booking
from users.models import Profile
from django.utils import timezone
from datetime import datetime

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-500"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-500"
        })
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["instructor", "lesson_type", "date", "time_slot"]

        widgets = {
            "instructor": forms.Select(attrs={
                "class": "w-full border rounded-md px-3 py-2"
            }),
            "lesson_type": forms.Select(attrs={
                "class": "w-full border rounded-md px-3 py-2"
            }),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full border rounded-md px-3 py-2"
            }),
            "time_slot": forms.Select(attrs={
                "class": "w-full border rounded-md px-3 py-2"
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only show users with role="Instructor"
        self.fields["instructor"].queryset = Profile.objects.filter(role="instructor")
        self.fields["instructor"].empty_label = "Select an Instructor"

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get("date")
        time_slot = cleaned_data.get("time_slot")

        if not date or not time_slot:
            return cleaned_data

        from django.utils import timezone
        from datetime import datetime

        now = timezone.localtime()
        today = now.date()

        # 🚫 Block past date
        if date < today:
            raise forms.ValidationError("You cannot book a past date.")

        # 🚫 If booking today, check time slot
        if date == today:
            start_time_str = time_slot.split("-")[0]
            selected_time = datetime.strptime(start_time_str, "%H:%M").time()

            if selected_time <= now.time():
                raise forms.ValidationError("This time slot has already passed.")

        return cleaned_data