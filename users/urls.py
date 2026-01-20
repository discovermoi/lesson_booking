from django.urls import path
from .views import signup_view
from .views import profile

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path('profile/', profile, name='profile'),
]
