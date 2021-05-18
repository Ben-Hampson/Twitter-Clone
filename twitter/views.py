from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView
from .models import Tweet
from .forms import TweetForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.safestring import mark_safe
from django.db.models import Q

# Create your views here.
class TweetListView(ListView):  # Homepage
    model = Tweet
    template_name = 'twitter/home.html'
    context_object_name = 'tweets'
    ordering = '-date_created'

    def get(self, request, *args, **kwargs):
        follows = request.user.profile.follows.count()
        explore_url = reverse('all-tweets')
        print(explore_url)
        if follows == 0:
            messages.add_message(request, messages.INFO, mark_safe(f"""Find some people to follow: <strong><a href="{explore_url}">Explore</a></strong>!"""))
        return super().get(request, *args, **kwargs)

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
        """If auth'd, only show tweets from authors the user follows.
        If not auth'd or a user has gone to 'explore', show all tweets."""
        if self.request.user.is_authenticated and self.request.path_info != reverse('all-tweets'):
            print(self.request.path_info)
            followees = self.request.user.profile.follows.all()
            q_followees = Q(author__in=followees)
            q_user = Q(author=self.request.user)
            queryset = Tweet.objects.filter(q_followees | q_user).all()
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
        user = self.request.user
        author = get_object_or_404(User, username=self.kwargs.get('username'))

        context['author'] = author
        context['user'] = user
        context['author_follows_count'] = author.profile.follows.count()
        context['author_followers_count'] = User.objects.filter(followers__user=user).count()
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Tweet.objects.filter(author=user).order_by('-date_created')

class HashtagListView(ListView):
    model = Tweet
    template_name = 'twitter/hashtag.html'
    context_object_name = 'tweets'

    def get_queryset(self):
        return get_list_or_404(Tweet, message__icontains=f"#{self.kwargs.get('hashtag')}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtag'] = self.kwargs.get('hashtag')
        return context