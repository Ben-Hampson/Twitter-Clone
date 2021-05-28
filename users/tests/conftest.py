import pytest
import factory
from pytest_factoryboy import register
from .factories import ProfileFactory, UserFactory

register(ProfileFactory)  # access fixture as profile_factory
register(UserFactory)


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
def user2(db, user_factory):
    user2 = user_factory.create(username="test_user2")
    return user2


@pytest.fixture
def profile(db, profile_factory):
    profile = profile_factory.create()
    return profile

@pytest.fixture
def profile2(db, profile_factory):
    profile = profile_factory.create(
        user = factory.SubFactory(UserFactory, username="profile_user2")
    )
    return profile