from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Profile

def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Puts the POST data into an instance of the form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def private_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('private-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

@login_required
def follow_user(request, user_pk):
    followee = get_object_or_404(User, id=user_pk)

    if user_pk != request.user.id:  # Check they're not trying to follow themselves.
        if followee.profile not in request.user.profile.follows.all():  # Check user is not already following the followee
            request.user.profile.follows.add(followee.profile.id)  # Note requires the profile ID, not the user ID.
            messages.success(request, f'You are now following @{followee.username}.')
        else:
            messages.warning(request, f"You already follow @{followee.username}!")
    else:
        messages.warning(request, "You can't follow yourself!")

    return redirect('public-profile', followee.username)

@login_required
def unfollow_user(request, user_pk):
    followee = get_object_or_404(User, id=user_pk)

    if user_pk != request.user.id:  # Check they're not trying to follow themselves.
        if followee.profile in request.user.profile.follows.all():  # Check user is not already following the followee
            request.user.profile.follows.remove(followee.profile.id)  # Note requires the profile ID, not the user ID.
            messages.success(request, f'You no longer follow @{followee.username}.')
        else:
            messages.warning(request, f"You already do not follow @{followee.username}!")
    else:
        messages.warning(request, "You can't unfollow yourself!")

    return redirect('public-profile', followee.username)

