from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Tweet

# Create your views here.
class TweetListView(ListView):
    model = Tweet
    template_name = 'twitter/tweet_list.html'
    context_object_name = 'tweets'
    ordering = '-date_created'