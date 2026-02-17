from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking
from django.contrib import messages
from django.core.mail import send_mail
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from .models import Booking


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def book_lesson(request):
    form = BookingForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        instructor = form.cleaned_data["instructor"]
        selected_date = form.cleaned_data["date"]
        selected_time = form.cleaned_data["time_slot"]

        # Get already booked slots
        booked_slots = Booking.objects.filter(
            instructor=instructor,
            date=selected_date
        ).values_list("time_slot", flat=True)

        # 🔒 Remove booked slots from dropdown
        available_slots = [
            slot for slot in Booking.TIME_SLOTS
            if slot[0] not in booked_slots
        ]

        form.fields["time_slot"].choices = available_slots

        if selected_time in booked_slots:
            form.add_error("time_slot", "This time slot is already booked.")
        else:
            booking = form.save(commit=False)
            booking.student = request.user.profile
            booking.save()
            return redirect("my_bookings")

    return render(request, "booking/book_lesson.html", {"form": form})


@login_required
def my_bookings(request):
    bookings = request.user.profile.student_bookings.all()
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

def create_checkout_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'aud',
                'product_data': {
                    'name': 'Lesson Booking',
                },
                'unit_amount': 5000,  # $50.00
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/booking/success/{booking.id}/'),
        cancel_url=request.build_absolute_uri('/booking/cancel/'),
    )

    return redirect(session.url)

# booking/views.py
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.payment_status = "PAID"
    booking.save()
    return render(request, "booking/payment_success.html", {"booking": booking})

def payment_cancel(request):
    return render(request, 'booking/payment_cancel.html')

@login_required
def payment_options(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student=request.user.profile)
    return render(request, "booking/payment_options.html", {"booking": booking})

@login_required
def pay_in_person(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.payment_status = "IN_PERSON"
    booking.save()

    messages.success(request, "Booking confirmed. Pay in person.")
    return redirect("my_bookings")


