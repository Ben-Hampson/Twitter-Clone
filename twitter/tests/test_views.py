import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from twitter import models
from twitter import forms
from pprint import pprint


class TestTweetListView:
    @pytest.mark.django_db
    def test_get_unauthenticated(self, client, tweet1, tweet2, tweet3, tweet4):
        """Test that an unauthenticated user sees all available tweets."""
        url = reverse("home")
        resp = client.get(url)

        tweets = resp.context_data["object_list"]

        assert resp.status_code == 200
        assert tweets.count() == 4

    def test_get_authenticated(self, client, profile, tweet1, tweet2, tweet3, tweet4):
        """Test that a new authenticated user sees zero tweets and is prompted to find people to follow."""
        client.force_login(profile.user)
        url = reverse("home")

        resp = client.get(url)
        tweets = resp.context_data["object_list"]
        message = [m.message for m in get_messages(resp.wsgi_request)][0]

        assert resp.status_code == 200
        assert tweets.count() == 0
        assert "Find some people to follow:" in message

    def test_TweetForm_in_context(self, client, profile):
        """Test that the TweetForm is passed through to the template."""
        client.force_login(profile.user)
        url = reverse("home")

        resp = client.get(url)
        form = resp.context_data["form"]

        assert resp.status_code == 200
        assert isinstance(form, forms.TweetForm)


class TestTweetDetailView:
    def test_TweetDetailView_instance(self, client, tweet1):
        """Test that the TweetDetailView displays a tweet."""
        url = reverse("tweet-detail", args={1})
        resp = client.get(url)

        tweet = resp.context_data["tweet"]

        assert resp.status_code == 200
        assert isinstance(tweet, models.Tweet)


class TestTweetDeleteView:
    @pytest.mark.django_db
    def test_TweetDeleteView_delete(self, client, tweet_factory, profile):
        """Test that an auth'd user can delete a tweet."""
        client.force_login(profile.user)
        tweet = tweet_factory(author=profile.user)

        url = reverse("tweet-delete", args={1})
        resp = client.get(url, follow=True)

        assert resp.status_code == 200
        assert "Are you sure you want to delete the tweet," in str(resp.content)


class TestUserTweetListView:
    def test_UserTweetListView_context(self, client, tweet_factory, profile, profile2):
        """Test that the user's tweets are returned."""
        client.force_login(profile.user)

        # Set up tweets. Only 2 should show on the profile page we visit.
        tweet1 = tweet_factory(author=profile.user)
        tweet2 = tweet_factory(author=profile.user)
        tweet3 = tweet_factory(author=profile2.user)

        # Visit public profile of 'profile'
        url = reverse("public-profile", args={profile.user.username})
        resp = client.get(url)

        tweets = resp.context_data["object_list"]

        assert resp.status_code == 200
        assert tweets.count() == 2


class TestHashtagListView:
    def test_HashtagListView_context(self, client, tweet_factory, profile):
        """Test that tweets with a specific hashtag show up in the hashtag list view."""
        client.force_login(profile.user)

        # Set up tweets. Only the first should show on the #food page.
        hashtag_tweet = tweet_factory(author=profile.user, message="I love #food")
        non_hashtag_tweet = tweet_factory(author=profile.user, message="I love food")

        # Visit public profile of 'profile'
        url = reverse("hashtag", args={"food"})
        resp = client.get(url)

        tweets = resp.context_data["tweets"]

        assert resp.status_code == 200
        assert len(tweets) == 1
