"""django_twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from twitter import views as twitter_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", twitter_views.TweetListView.as_view(), name="home"),
    path("explore/", twitter_views.TweetListView.as_view(), name="all-tweets"),
    path("register/", user_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("profile/", user_views.private_profile, name="private-profile"),
    path(
        "tweet/<int:pk>/", twitter_views.TweetDetailView.as_view(), name="tweet-detail"
    ),
    path(
        "<str:username>/",
        twitter_views.UserTweetListView.as_view(),
        name="public-profile",
    ),
    path(
        "hashtag/<str:hashtag>/",
        twitter_views.HashtagListView.as_view(),
        name="hashtag",
    ),
    path(
        "delete/<int:pk>/", twitter_views.TweetDeleteView.as_view(), name="tweet-delete"
    ),
    path("<str:username>/follow/", user_views.follow_user, name="follow-user"),
    path("<str:username>/unfollow/", user_views.unfollow_user, name="unfollow-user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
