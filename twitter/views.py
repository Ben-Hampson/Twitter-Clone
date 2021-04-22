from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Tweet
from .forms import TweetForm
from django.contrib.auth.models import User

# Create your views here.
class TweetListView(ListView):
    model = Tweet
    template_name = 'twitter/home.html'
    context_object_name = 'tweets'
    ordering = '-date_created'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TweetForm()
        return context
    
    def post(self, request):
        form = TweetForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return redirect('tweet-detail')

class TweetDetailView(DetailView):
    model = Tweet
    context_object_name = 'tweet'

class UserTweetListView(ListView):
    model = Tweet
    template_name = 'twitter/public_profile.html'
    context_object_name = 'tweets'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Tweet.objects.filter(author=user).order_by('-date_created')