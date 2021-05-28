from django.urls import reverse
from django.contrib.messages import get_messages
import pytest
from pprint import pprint


class TestUserViews:
    @pytest.mark.django_db
    def test_register_view(self, client):
        """Test that a user can sign up."""
        url = reverse("register")
        data = {
            "username": "twixtwenty",
            "email": "email@email.com",
            "password1": "aahlskdjfa",
            "password2": "aahlskdjfa",
        }

        resp = client.post(url, data, follow=True)  # Follow through redirects
        message = [m.message for m in get_messages(resp.wsgi_request)][0]

        assert resp.status_code == 200
        assert message == "Account created for twixtwenty"

    def test_private_profile_view(self, client, profile):
        """Test a user can update their profile."""
        client.force_login(profile.user)

        url = reverse("private-profile")
        data = {
            "email": "updated-email@email.com",
            "display_name": "example_display_name",
        }

        resp = client.post(url, data, follow=True)
        message = [m.message for m in get_messages(resp.wsgi_request)][0]

        assert resp.status_code == 200
        assert message == "Your account has been updated!"

    def test_follow_user_view(self, client, profile, profile2):
        """Test a user can follow another user."""
        client.force_login(profile.user)

        url = reverse("follow-user", args=[profile2.user.username])

        resp = client.get(url, follow=True)
        message = [m.message for m in get_messages(resp.wsgi_request)][0]

        assert resp.status_code == 200
        assert message == "You are now following @profile_user2."

    def test_unfollow_user_view(self, client, profile, profile2):
        """Test a user can unfollower another user."""
        client.force_login(profile.user)
        profile.follows.set([profile2.user.id])

        url = reverse("unfollow-user", args=[profile2.user.username])

        resp = client.get(url, follow=True)
        message = [m.message for m in get_messages(resp.wsgi_request)][0]

        assert resp.status_code == 200
        assert message == "You no longer follow @profile_user2."
