from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from .models import Tweet
from .forms import TweetForm

# Create your views here.
class TweetListView(ListView):
    model = Tweet
    template_name = 'twitter/tweet_list.html'
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