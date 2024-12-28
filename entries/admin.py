from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from .models import Entry



class EntryAdmin(admin.ModelAdmin):
    """ Filter Entries For Admin Dashbaord """

    # Fields to display
    list_display = ('content_shorted', 'profile_link', 'user_link', 'date_created', 'mood', 'reads', 'likes', 'reported', 'featured')

    # Filters available
    list_filter = ('reported', 'featured')

    # Readonly fields
    readonly_fields = ('content', 'mood', 'likes', 'reads')

    # Search fields
    search_fields = ('user__username', 'content',)

    # Queryset
    def get_queryset(self, request):
    	# Only public and reported entries could be seen by DG.
        qs = super(EntryAdmin, self).get_queryset(request)
        return qs.filter(Q(user__profile__public=True)|Q(reported=True)) 

    def profile_link(self, obj):
    	return format_html(f'<a href="/go_to/the_site_adminstration_panel/users/profile/{obj.user.profile.id}/change/">Profile</a>')

    def user_link(self, obj):
    	return format_html(f'<a href="/go_to/the_site_adminstration_panel/auth/user/{obj.user.id}/change/">{obj.user}</a>')

    def content_shorted(self, obj):
    	return obj.content[:50]


admin.site.register(Entry, EntryAdmin)     