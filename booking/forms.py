from django import forms
from .models import Booking

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
        # Filter instructors
        self.fields['instructor'].queryset = Booking._meta.get_field('instructor').remote_field.model.objects.filter(role="INSTRUCTOR")
