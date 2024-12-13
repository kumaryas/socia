from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Jab User create ho, tab Profile model automatically create ho
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Sirf jab user naya ho
        Profile.objects.create(user=instance)

# Jab User save ho, tab uska Profile bhi save ho
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()  # Try to save the profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)  # Agar profile exist nahi karti toh create karna
