from django.db import models
from users.models import Profile

class Booking(models.Model):
    PAYMENT_STATUS = [
        ("UNPAID", "Unpaid"),
        ("PAID", "Paid"),
        ("IN_PERSON", "Pay in person"),
    ]

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="UNPAID"
    )

    TIME_SLOTS = [
        ("09:00", "09:00 AM"),
        ("10:00", "10:00 AM"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    LESSON_TYPES = [
        ("FREE", "Free Intro (15 mins)"),
        ("45", "45 Minutes"),
        ("60", "60 Minutes"),
        ("90", "90 Minutes"),
    ]

    lesson_type = models.CharField(
        max_length=10,
        choices=LESSON_TYPES,
        default="60",
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )

    paid = models.BooleanField(default=False)

    instructor = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'instructor'},
    )
    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="student_bookings"
    )
    date = models.DateField()
    time_slot = models.CharField(
        max_length=20,
        choices=TIME_SLOTS,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} → {self.instructor.user.username} on {self.date} at {self.time_slot}"
