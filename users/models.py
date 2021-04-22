from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=40)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=280)
    location = models.CharField(max_length=140)
    website = models.CharField(max_length=280)

    def __str__(self):
        return f"{self.user.username} Profile"