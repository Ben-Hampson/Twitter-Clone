import factory

from django.contrib.auth.models import User
from users.models import Profile
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = 'test_user'

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, username='profile_user')
    display_name = 'test_profile'