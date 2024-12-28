from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse


from users.models import Profile
from .models import Entry
from notifications.models import Notification
from .forms import EntryForm
from khandiary.privacy_check import privacy_check


@login_required
def entries(request, user=None):
    """Show user's all entries."""

    if user:
        user = get_object_or_404(User, username=user)
    else:
        user = request.user
        
    profile = user.profile

    if privacy_check(request, profile) == "green":
        entries = Entry.objects.filter(user=user).order_by('-date_created')
    else:
        return render(request, 'users/private_account_message.html')

    entries_count = entries.count()

    context = {'title': f"{user} - Entries", 'entries': entries,
               'entries_count': entries_count}

    return render(request, 'entries/entries.html', context)



@login_required
def search_user_entry(request, user):
    """ Search within user's enrtries. """

    user = get_object_or_404(User, username=user)
    query = request.GET['entry_query']

    if privacy_check(request, user.profile) == "green":

        if len(query) >= 3 and len(query) <= 70:
            entries = Entry.objects.filter(
                user=user, content__icontains=query)
            entries_count = entries.count()
        else:
            entries = ''
            entries_count = 0

        context = {'title': f"{user} - {query}",
                   'user': user,
                   'entries': entries,
                   'entries_count': entries_count,
                   'searched_query': query,
                   }
        return render(request, 'entries/search_user_entry.html', context)

    else:
        return render(request, 'users/private_account_message.html')


@login_required
def add_read(request, entry_id):
    """ Add Read to the Entry """

    if request.method == "POST":
        response_data = {}
        profile = request.user.profile

        if Entry.objects.filter(id=entry_id).exists():
            entry = Entry.objects.get(id=entry_id)
            if privacy_check(request, entry.user.profile) == "green":

                # Add +1 read & add entry to the user's Read History.
                if entry not in profile.read_history.all():
                    entry.reads =+ 1
                    entry.save()

                    profile.read_history.add(entry)
                    profile.save()

                    response_data['status'] = "+1 Read"
            else:
                response_data['status'] = 'error'
        else:
            response_data['status'] = 'error'

        return JsonResponse(response_data)
    else:
        raise Http404

from datetime import datetime
@login_required
def add_entry(request):
    """Add new entry."""

    user = request.user
    profile = user.profile

    # Make sure user does not add entry before 24 hours.
    can_add = True
    
    if Entry.objects.filter(user=user).count() > 0:
        previous_entry = Entry.objects.filter(user=user).order_by('-date_created').first()
        elapsed_time = datetime.now().hour - previous_entry.date_created.hour
        if elapsed_time <= 0:
            can_add = False

    if request.method == "POST":
        form = EntryForm(request.POST)
        if profile.banned == False and can_add:
            if form.is_valid:
                entry = form.save(commit=False)
                entry.user = user
                entry.save()

                messages.success(
                    request, 'Your entry has been added succesfully !')
                return redirect('entries:entries', user=user)
            else:
                messages.error(request, 'Unable to add, an error occured !')
        else:
            messages.error(request, 'Unable to add, an error occured !')
    else:
        form = EntryForm()

    context = {'title': "New entry", 'form': form,
               'profile': profile, 'can_add': can_add}

    return render(request, 'entries/new_entry.html', context)



@login_required
def entry(request, entry_id):
    """Entry detailed."""

    entry = get_object_or_404(Entry, id=entry_id)

    if privacy_check(request, entry.user.profile) == "green":
        user = entry.user
        date = entry.date_created.strftime('%d %B %Y %H:%M %p')  # For Tab

        # Next and Prevoius entries.
        if Entry.objects.filter(user=entry.user, id__lt=entry.id).order_by('-id').exists():
            previous_entry = Entry.objects.filter(user=entry.user, id__lt=entry.id).order_by('-id').first()
        else:
            previous_entry = None

        if Entry.objects.filter(user=entry.user, id__gt=entry.id).order_by('id').exists():
            next_entry = Entry.objects.filter(user=entry.user, id__gt=entry.id).order_by('id').first()
        else:
            next_entry = None


        context = {'title': f" {user} - {date}", 'entry': entry, 'previous_entry': previous_entry, 'next_entry': next_entry}

        return render(request, 'entries/entry.html', context)

    else:
        return render(request, 'entries/private_entry_message.html')



@login_required
def edit_entry(request, entry_id):
    """Edit existing entry."""

    entry = get_object_or_404(Entry, id=entry_id)

    if entry.user == request.user:

        if request.method == "POST":
            form = EntryForm(instance=entry, data=request.POST)
            if form.is_valid():
                entry = form.save()

                messages.success(
                    request, 'Your entry has been edited succesfully !')
                return redirect('diary:entry', entry_id=entry.id)
            else:
                messages.error(request, 'Unable to edit, an error occured !')
        else:
            form = EntryForm(instance=entry)

        date = entry.date_created.strftime('%d %B %Y %H:%M %p')

        context = {'title': f" Edit Entry - {date}",
                   'form': form}

        return render(request, 'entries/edit_entry.html', context)
    else:
        raise Http404


@login_required
def like_entry(request, entry_id):
    """Like Entry"""

    if request.method == "POST":
        response_data = {}
        profile = request.user.profile

        if Entry.objects.filter(id=entry_id).exists():
            entry = Entry.objects.get(id=entry_id)
            preview = entry.content[:70] #For noti.

            if entry not in profile.liked_entries.all():
                if entry.user.profile.public and entry.user != request.user:
                    profile.liked_entries.add(entry)
                    profile.save()
                    entry.likes += 1
                    entry.save()
                    response_data['status'] = 'liked'

                    # Add noti (Make sure that noti don't go to user itself).
                    if entry.user != request.user:
                        Notification.objects.create(entry=entry, sender=request.user, user=entry.user, preview=preview, notification_type=2)

                else:
                    response_data['status'] = 'error'
            else:
                profile.liked_entries.remove(entry)  # Remove anyway.
                profile.save()
                entry.likes -= 1
                entry.save()
                response_data['status'] = 'unliked'

                # Delete noti.
                noti = Notification.objects.filter(entry=entry, sender=request.user, user=entry.user, preview=preview,  notification_type=2)
                noti.delete()

        else:
            response_data['status'] = 'error'

        likes_count = entry.likes
        response_data['likes_count'] = likes_count

        liked_entries_count = profile.liked_entries.all().count()
        response_data['liked_entries_count'] = liked_entries_count

        return JsonResponse(response_data)
    else:
        raise Http404


@login_required
def save_entry(request, entry_id):
    """Save Entry"""

    if request.method == "POST":
        response_data = {}
        profile = request.user.profile

        if Entry.objects.filter(id=entry_id).exists():
            entry = Entry.objects.get(id=entry_id)

            if entry not in profile.saved_entries.all():
                if privacy_check(request, profile) == "green":
                    profile.saved_entries.add(entry)
                    profile.save()
                    response_data['status'] = 'saved'
                else:
                    response_data['status'] = 'error'
            else:
                profile.saved_entries.remove(entry)  # Remove anyway.
                profile.save()
                response_data['status'] = 'unsaved'

        else:
            response_data['status'] = 'error'

        saved_entries_count = profile.saved_entries.all().count()
        response_data['saved_entries_count'] = saved_entries_count

        return JsonResponse(response_data)
    else:
        raise Http404



@login_required
def report_entry(request, entry_id):
    """Report Entry"""

    if request.method == "POST":
        response_data = {}

        if Entry.objects.filter(id=entry_id).exists():
            entry = Entry.objects.get(id=entry_id)

            if not entry.reported:
                # As user can't report own entyry.
                if entry.user.profile.public and entry.user != request.user:
                    entry.reported = True
                    entry.save()
                    response_data['status'] = 'reported'
                else:
                    response_data['status'] = 'error'
            else:
                response_data['status'] = 'already_reported'
        else:
            response_data['status'] = 'error'

        return JsonResponse(response_data)
    else:
        raise Http404


@login_required
def delete_entry(request, entry_id):
    """Delete Entry"""

    if request.method == "POST":
        response_data = {}

        if Entry.objects.filter(id=entry_id, user=request.user).exists():
            entry = Entry.objects.get(id=entry_id)
            entry.delete()
            response_data['status'] = "deleted"
        else:
            response_data['status'] = 'error'

        return JsonResponse(response_data)
    else:
        raise Http404



@login_required
def mood(request, mood, user=None):
    """ Explore by mood page """

    mood = mood 
    
    if user:
        user = get_object_or_404(User, username=user) 

    if not user:
        entries = Entry.objects.filter(mood=mood, user__profile__public=True).order_by('-date_created')
    else:
        if privacy_check(request, user.profile) == "green":
            entries = Entry.objects.filter(mood=mood, user=user).order_by('-date_created')
        else:
            return render(request, 'users/private_account_message.html')

    context = {'title': f"Mood - {mood}", 'mood': mood, 'entries': entries}

    return render(request, 'entries/mood.html', context)




@login_required
def most_liked_entries(request):
    """Show most liked entries."""

    entries = Entry.objects.filter(user__profile__public=True).order_by('-likes')

    context = {'entries': entries}

    return render(request, 'entries/most_liked_entries.html', context)


@login_required
def most_viewed_entries(request):
    """Show most viewed entries."""

    entries = Entry.objects.filter(user__profile__public=True).order_by('-reads')

    context = {'entries': entries}

    return render(request, 'entries/most_viewed_entries.html', context)



@login_required
def saved_entries(request):
    """Show user's all saved entries."""

    user = request.user

    entries = user.profile.saved_entries.all()
    entries_count = entries.count()

    context = {'title': "Saved Entries", 'entries': entries,
               'entries_count': entries_count}

    return render(request, 'entries/saved_entries.html', context)


@login_required
def liked_entries(request):
    """Show user's all liked entries."""

    user = request.user

    entries = user.profile.liked_entries.all()
    entries_count = entries.count()

    context = {'title': "Liked Entries", 'entries': entries,
               'entries_count': entries_count}

    return render(request, 'entries/liked_entries.html', context)


@login_required
def read_history(request):
    """Read History."""

    user = request.user

    entries = user.profile.read_history.all()
    entries_count = entries.count()

    context = {'title': "Read History", 'entries': entries,
               'entries_count': entries_count}

    return render(request, 'entries/read_history.html', context)


@login_required
def clear_read_history(request):
    """Clear Read History """

    if request.method == "POST":
        profile = request.user.profile

        entries = profile.read_history.all()
        for entry in entries:
            entry.reads -= 1
            entry.save()
            profile.read_history.remove(entry)

        profile.save()    
        messages.success(request, f'Your read history has been cleared successfully.')
        return redirect('entries:read_history')
    else:
        Http404  






