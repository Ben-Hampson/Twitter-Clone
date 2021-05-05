from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView
from .models import Tweet
from .forms import TweetForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

# Create your views here.
class TweetListView(ListView):  # Homepage
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
        return redirect('home')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            followees = self.request.user.profile.follows.all()
            print(followees)
            q_followees = Q(author__in=followees)
            q_user = Q(author=self.request.user)
            queryset = Tweet.objects.filter(q_followees | q_user).all()
            print(queryset)
        else:
            queryset = super().get_queryset()
        return queryset

class TweetDetailView(DetailView):
    model = Tweet
    context_object_name = 'tweet'

class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        tweet = self.get_object()
        if self.request.user == tweet.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Tweet deleted.')
        return super().delete(request, *args, **kwargs)

class UserTweetListView(ListView):  # Public Profile
    model = Tweet
    template_name = 'twitter/public_profile.html'
    context_object_name = 'tweets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(User, username=self.kwargs.get('username'))
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Tweet.objects.filter(author=user).order_by('-date_created')

class HashtagListView(ListView):
    model = Tweet
    template_name = 'twitter/public_profile.html'
    context_object_name = 'tweets'

    def get_queryset(self):
        return get_list_or_404(Tweet, message__icontains=f"#{self.kwargs.get('hashtag')}")