from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('Instructor', 'Instructor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    # You can add first_name, last_name if you like, but User model already has them

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Signal to automatically create Profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save Profile when User is saved
    @receiver(post_save, sender=User)
    def ensure_profile_exists(sender, instance, created, **kwargs):
        Profile.objects.get_or_create(user=instance)

