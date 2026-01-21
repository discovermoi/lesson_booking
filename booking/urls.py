from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_lesson, name='book_lesson'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
]
