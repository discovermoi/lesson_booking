from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking
from django.contrib import messages

@login_required
def book_lesson(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            booking.save()
            messages.success(request, "Booking created successfully!")
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'booking/book_lesson.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = request.user.bookings_made.all()
    return render(request, 'booking/my_bookings.html', {'booking': bookings})
