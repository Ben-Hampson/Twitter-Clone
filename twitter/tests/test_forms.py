from twitter import forms


class TestTweetForm:
    def test_TweetForm_tweet(self):
        """Test posting a tweet message through the form."""
        data = {"message": "This is a test tweet!"}
        form = forms.TweetForm(data=data)
        assert form.is_valid()
