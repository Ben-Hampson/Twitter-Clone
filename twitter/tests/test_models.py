import pytest
import datetime
from .factories import TweetFactory
from django.contrib.auth.models import User


class TestTweet:
    def test_Tweet(self, tweet1):
        """Test that a new Tweet can be instantiated as expected."""
        assert isinstance(tweet1.author, User)
        assert tweet1.message == "Tweet message"
        assert isinstance(tweet1.date_created, datetime.datetime)
