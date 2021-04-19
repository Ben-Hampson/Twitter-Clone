from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # If the 'many' part (User) is deleted, the waterfall of destruction cascades down and washes away the 'one' (Tweets)  too.
    message = models.CharField(max_length=280)
    date_created = models.DateTimeField(auto_now=True)
