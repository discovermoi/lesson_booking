from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_lesson, name='book_lesson'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path("booking/<int:booking_id>/payment/", views.payment_options, name="booking_payment_options"),
    path('checkout/<int:booking_id>/', views.create_checkout_session, name='checkout'),
    path("booking/<int:booking_id>/pay-in-person/",views.pay_in_person,name="pay_in_person"),
    path("booking/<int:booking_id>/pay-in-person/", views.pay_in_person, name="pay_in_person"),
]
