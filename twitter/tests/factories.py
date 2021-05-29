import factory
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from twitter.models import Tweet


class TweetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tweet

    author = factory.SubFactory("users.tests.factories.UserFactory")
    message = "Tweet message"
    date_created = datetime.datetime.now(datetime.timezone.utc)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_user"
    password = "askdl;fa"
