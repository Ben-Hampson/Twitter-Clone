from django.forms import ModelForm, Textarea
from .models import Tweet

class TweetForm(ModelForm):

    class Meta:
        model = Tweet
        fields = ['message']
        widgets = {
            'message': Textarea(attrs={
                'class': 'textarea is-info has-fixed-size',
                'rows': '2',
                'placeholder': "What's happening?"}),
        }