from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking
from django.contrib import messages
from django.core.mail import send_mail

@login_required
def book_lesson(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user.profile
            booking.save()

            send_mail(
                subject="New Lesson Booking",
                message=(
                    f"You have a new booking!\n\n"
                    f"Student: {booking.student.user.username}\n"
                    f"Date: {booking.date}\n"
                    f"Time: {booking.time_slot}"
                ),
                from_email=None,
                recipient_list=[booking.instructor.user.email],
            )

            messages.success(request, "Booking created successfully!")
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'booking/book_lesson.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = request.user.profile.student_bookings.all()
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


