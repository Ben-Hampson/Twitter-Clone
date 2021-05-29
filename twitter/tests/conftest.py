from twitter.models import Tweet
import pytest
from pytest_factoryboy import register
from .factories import TweetFactory
from users.tests.factories import UserFactory, ProfileFactory
import factory

register(TweetFactory)  # access fixture as tweet_factory
register(UserFactory)
register(ProfileFactory)


@pytest.fixture
def user1(db, user_factory):
    user1 = user_factory.create(
        username="test_user1",
        email="username123@example.com",
        # password1="testtest",
        # password2="testtest"
    )
    return user1


@pytest.fixture
def profile(db, profile_factory):
    profile = profile_factory.create()
    return profile


@pytest.fixture
def profile2(db, profile_factory):
    profile = profile_factory.create(
        user=factory.SubFactory(UserFactory, username="profile_user2")
    )
    return profile


@pytest.fixture
def tweet1(db, tweet_factory, user1):
    tweet1 = tweet_factory.create(author=user1)
    return tweet1


@pytest.fixture
def tweet2(db, tweet_factory, user1):
    tweet2 = tweet_factory.create(author=user1)
    return tweet2


@pytest.fixture
def tweet3(db, tweet_factory, user1):
    tweet3 = tweet_factory.create(author=user1)
    return tweet3


@pytest.fixture
def tweet4(db, tweet_factory, user1):
    tweet4 = tweet_factory.create(author=user1)
    return tweet4
