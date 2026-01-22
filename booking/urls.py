from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_lesson, name='book_lesson'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('book/', views.book_lesson, name='book_lesson'),
    path('checkout/<int:booking_id>/', views.create_checkout_session, name='checkout'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]
