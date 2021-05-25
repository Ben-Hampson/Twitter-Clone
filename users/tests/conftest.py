import pytest

from pytest_factoryboy import register
from users.tests.factories import ProfileFactory#, UserFactory

register(ProfileFactory)  # access fixture as profile_factory
# register(UserFactory)

# @pytest.fixture
# def user(db, user_factory):
#     user = user_factory.create()
#     return user

@pytest.fixture
def profile(db, profile_factory):
    profile = profile_factory.create()
    return profile