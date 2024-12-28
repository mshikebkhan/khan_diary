from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404

from .send_welcome_email import send_welcome_email
from entries.models import Entry
from notifications.models import Notification
from .get_mood_stats import get_mood_stats
from khandiary.privacy_check import privacy_check
from .forms import SignupForm, ProfileUpdateForm, UserUpdateForm, ChangePasswordForm, AccountPrivacyForm



def signup(request):
    """ Register new user. """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            new_user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)

            # Send welcome email
            send_welcome_email(first_name, email)
            
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            messages.success(
                request, f'{first_name} your account has been created successfully. Please setup your profile!')

            return redirect('users:edit-profile')

        else:
            first_name = form.data.get('first_name')
            last_name = form.data.get('last_name')
            username = form.data.get('username')
            email = form.data.get('email')
            password1 = form.data.get('password1')
            messages.error(
                request, f'Unable to create  account! Please correct the errors below.')

    else:
        form = SignupForm()
        first_name = ''
        last_name = ''
        username = ''
        email = ''
        password1 = ''

    context = {
        'title': "Sign Up", 'form': form,
        'first_name': first_name, 'last_name': last_name, 'username': username,
        'email': email, 'password1': password1
    }

    return render(request, 'users/signup.html', context)


@login_required
def profile(request, user=None):
    """Profile Page"""
    if user:
        user = get_object_or_404(User, username=user)
    else:
        user = request.user
        
    profile = user.profile

    if privacy_check(request, profile) == "green":

        entries = Entry.objects.filter(user=user).order_by('-date_created')

        # A dict of % of moods in user's entries for bar width in profile page.
        mood_stats = get_mood_stats(entries)

        context = {'title': f"{user} - Profile",
                   'profile': profile, 'mood_stats': mood_stats}

        return render(request, 'users/profile.html', context)
    else:
        return render(request, 'users/private_account_message.html')


@login_required
def follow_user(request, user_id):
    """User User"""
    if request.method == "POST":
        response_data = {}
        profile = request.user.profile

        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)

            if user not in profile.following.all():
                if user != request.user and user.profile.public:
                    profile.following.add(user)
                    profile.save()

                    # Add current user to user's followers.
                    user.profile.followers.add(request.user)
                    user.profile.save()

                    # Add noti.
                    Notification.objects.create(sender=request.user,
                    user=user, notification_type=3)

                    response_data['status'] = 'followed'
                else:
                    response_data['status'] = 'private_profile'
            else:
                profile.following.remove(user)  # Unfollow.
                profile.save()

                # Remove current user from user's followers.
                user.profile.followers.remove(request.user)
                user.profile.save()

                noti = Notification.objects.filter(sender=request.user,
                user=user, notification_type=3)
                noti.delete()

                response_data['status'] = 'unfollowed'

        else:
            response_data['status'] = 'not_exists'

        followers_count = user.profile.followers.all().count()
        response_data['followers_count'] = followers_count

        following_count = profile.following.all().count()
        response_data['following_count'] = following_count

        return JsonResponse(response_data)
    else:
        raise Http404


@login_required
def followers(request, user):
    """Followers Page"""

    user = get_object_or_404(User, username=user)
    profile = user.profile

    if privacy_check(request, profile) == "green":

        followers = profile.followers.all()
        followers_count = followers.count()

        context = {'title': f"{user} - Followers",
                   'users': followers, 'followers_count': followers_count}

        return render(request, 'users/followers.html', context)
    else:
        return render(request, 'users/private_account_message.html')


@login_required
def following(request, user):
    """Following Page"""
    user = get_object_or_404(User, username=user)
    profile = user.profile

    if privacy_check(request, profile) == "green":

        following = profile.following.all()
        following_count = following.count()

        context = {'title': f"{user} - Following",
                   'users': following, 'following_count': following_count}

        return render(request, 'users/following.html', context)
    else:
        return render(request, 'users/private_account_message.html')


@login_required
def most_popular_users(request):
    users = User.objects.filter(profile__public=True).order_by('-followers')
        
    context = {'users': users}

    return render(request, 'users/most_popular_users.html', context)



@login_required
def edit_profile(request):
    """ Settings Page / Edit profile """

    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(
                request, f'Profile has been updated successfully.')
            return redirect('users:profile', user=request.user)
        else:
            messages.error(
                request, f' Unable to update profile. Please correct the error below.')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': "Edit profile",
        'uform': uform,
        'pform': pform
    }

    return render(request, 'users/edit-profile.html', context)


@login_required
def account(request):
    """Settings Page / Account settings"""
    profile = request.user.profile

    context = {'title': "Account"}

    return render(request, 'users/account.html', context)


@login_required
def change_password(request):
    """ Change Password """
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            authenticated_user = authenticate(username=request.user.username,
                                              password=request.POST['new_password'])
            login(request, authenticated_user)
            messages.success(
                request, 'Your password has been updated successfully.')

            return redirect('users:account')
        else:
            old_password = form.data.get('old_password')
            messages.error(
                request, f'Unable to update the password! Please correct the errors below.')
            
    else:
        form = ChangePasswordForm(instance=user)
        old_password = ''

    context = {
        'title': "Change Password", 'form': form, 'old_password': old_password
    }

    return render(request, 'users/change_password.html', context)


@login_required
def security_checkup(request):
    """ Shows last login """
    user = request.user

    last_login = user.last_login

    context = {'title': "Security Checkup", 'last_login': last_login}

    return render(request, 'users/security_checkup.html', context)



@login_required
def account_privacy_setting(request):
    """ Account privacy setting """
    public = request.user.profile.public

    if request.method == 'POST':
        form = AccountPrivacyForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(
                request, f'Account privacy setting has been updated successfully.')
            return redirect('users:account')
        else:
            messages.error(
                request, f' Unable to update setting. Please correct the error below.')
    else:
        form = AccountPrivacyForm(instance=request.user.profile)

    context = {
        'title': "account privacy settings",
        'form': form,
        'public': public
    }

    return render(request, 'users/account_privacy_setting.html', context)


def logout(request):
    """Log out the user"""
    if request.user.is_authenticated:
        django_logout(request)
        messages.success(
            request, 'You have been logged out successfully!')
        return redirect('core:index')
    else:
        raise Http404
