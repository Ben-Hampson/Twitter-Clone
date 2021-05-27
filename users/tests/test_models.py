import pytest

# from factories import UserFactory, ProfileFactory
from users import models


class TestProfile:
    @pytest.mark.django_db
    def test_Profile_instance(self, profile):
        """Test that a new User creates and binds to a new Profile"""
        assert isinstance(profile, models.Profile)

    @pytest.mark.django_db
    def test_Profile_str(self, profile_factory):
        """Test that the string representation of a Profile is the User username."""
        assert profile_factory().__str__() == "profile_user Profile"

    @pytest.mark.django_db
    def test_Profile_follow(self, profile, user1):
        """Test that a Profile can follow a User"""
        profile.follows.add(user1.id)
        assert profile.follows.count() == 1

    @pytest.mark.django_db
    def test_Profile_unfollow(self, profile, user1):
        """Test that a Profile can unfollow a User"""
        profile.follows.set([user1.id])
        profile.follows.remove(user1.id)
        assert profile.follows.count() == 0

    # def test_profile_update(self, user, profile):
    #     """ Test that a Profile can be updated. """

    #     assert user.username == 'test_user'
    #     assert profile.display_name == 'test_profile'
    # assert profile.follows.count() == 1

    # def test_Profile_unfollow():

    # def test_Profile_update():
