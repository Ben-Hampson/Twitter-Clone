import pytest
# from factories import UserFactory, ProfileFactory

class TestProfile:

    @pytest.mark.django_db
    def test_Profile_follow(self, profile):
        """ Test that a Profile can follow a User. """
        # user = user_factory.build()
        # profile = profile_factory.build()
        
        # profile.follows.set(user)
        print(profile.user)
        
        assert profile.display_name == 'test_profile'

    # def test_profile_update(self, user, profile):
    #     """ Test that a Profile can be updated. """
        
    #     assert user.username == 'test_user'
    #     assert profile.display_name == 'test_profile'
        # assert profile.follows.count() == 1


    # def test_Profile_unfollow():


    # def test_Profile_update():