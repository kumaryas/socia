from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instagram_access_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_access_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_access_token_secret = models.CharField(max_length=255, blank=True, null=True)
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"