from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, Http404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as django_logout

from .feed_maker import feed_maker
from entries.models import Entry
import datetime

def documentation(request):
    """ Documentation page """
    context = {'title': "Documentation"}
    return render(request, 'khandiary/documentation.html', context)

@login_required
def index(request):
    entries = feed_maker(request)
    entries_count = len(entries)

    if request.user_agent.is_mobile:
        tab_size = "is-small"
    else:
        tab_size = ""

    current_hour = datetime.datetime.now().hour
    context = {'entries': entries, 'entries_count': entries_count,
     'tab_size': tab_size, 'current_hour': current_hour}

    return render(request, 'khandiary/index.html', context)


def about(request):
    """About us page"""
    context = {'title': "About us"}
    return render(request, 'khandiary/about.html', context)


def faq(request):
    """FAQ page"""
    context = {'title': "FAQ"}
    return render(request, 'khandiary/faq.html', context)


def privacy(request):
    """Privacy Policy page"""
    context = {'title': "Privacy Policy"}
    return render(request, 'khandiary/privacy.html', context)


def terms(request):
    """Terms & Conditions page"""
    context = {'title': "Terms & Conditions"}
    return render(request, 'khandiary/terms.html', context)

def contact(request):
    """Contact us page (with message functionality)"""
    context = {'title': "Contact us"}
    return render(request, 'khandiary/contact.html', context)


@login_required
def explore(request):
    """Search within diary entries."""

    # Count users whose profile is public
    total_users_count = User.objects.filter(profile__public=True).count()

    # Count entries that belong to users with public profiles
    total_entries_count = Entry.objects.filter(user__profile__public=True).count()

    context = {'title': "Explore", 'total_users_count': total_users_count, 'total_entries_count': total_entries_count}
    return render(request, 'khandiary/explore.html', context)


@login_required
def search_user_or_entry(request, option):
    """ Search for User or Entry. """
    users = None
    entries = None 
    option = option
    query = request.GET['query']

    if option == 1:
        if len(query) >= 2 and len(query) <= 70:
            users = User.objects.filter(
                username__icontains=query,
                profile__public=True)

        template = 'khandiary/search_user.html'

    else:
        if len(query) >= 2 and len(query) <= 70:
            entries = Entry.objects.filter(
                content__icontains=query,
                user__profile__public=True)

        template = 'khandiary/search_entry.html'

    context = {'title': f"Search - {query}",
               'users': users,
               'entries': entries,
               'searched_query': query,
               }
    return render(request, template, context)


def logout(request):
    """Log out the user"""
    if request.user.is_authenticated:
        django_logout(request)
        messages.success(
            request, 'You have been logged out successfully!')
        return redirect('khandiary:index')
    else:
        raise Http404
