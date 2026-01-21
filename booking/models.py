from django.db import models
from users.models import Profile

class Booking(models.Model):
    TIME_SLOTS = [
        ("09:00-10:00", "09:00 – 10:00"),
        ("10:00-11:00", "10:00 – 11:00"),
        ("11:00-12:00", "11:00 – 12:00"),
        ("14:00-15:00", "14:00 – 15:00"),
    ]

    instructor = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'INSTRUCTOR'}
    )
    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="student_bookings"
    )
    date = models.DateField()
    time_slot = models.CharField(
        max_length=20,
        choices=TIME_SLOTS
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} -> {self.instructor.user.username} on {self.date} at {self.time_slot}"
