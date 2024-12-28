from entries.models import Entry

def feed_maker(request):
	""" Entries for the current user. """
	profile = request.user.profile

	all_entries = set(Entry.objects.all().values_list('id', flat=True))
	read_history = set(profile.read_history.all().values_list('id', flat=True))

	entries = all_entries-read_history

	following_users = profile.following.filter(profile__public=True).values_list('id', flat=True)
	
	entries_from_users = Entry.objects.filter(id__in=entries, user__id__in=following_users).order_by('-date_created')

	entries = set(entries_from_users)

	return entries

