from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils.html import format_html

from .models import Profile



class ProfileAdmin(admin.ModelAdmin):
    """ Filter Profiles For Admin Dashbaord """

    # Fields to display
    list_display = ('profile', 'user_link', 'gender', 'country', 'followers_count', 'following_count', 'public', 'banned', 'verified')

    # Filters available
    list_filter = ('gender', 'country',  'public', 'banned', 'verified')

    # Readonly fields
    readonly_fields = ('birthday', 'bio', 'facebook', 'twitter', 'instagram', 'youtube', 'gender', 'country', 'saved_entries', 'liked_entries', 'read_history', 'followers', 'following', 'public', 
        )

    # Search fields
    search_fields = ('user__username',)

    # Queryset
    def followers_count(self, obj):
    	return obj.followers.all().count()

    def following_count(self, obj):
    	return obj.following.all().count()

    def profile(self, obj):
    	return format_html(f'<a href="/go_to/the_site_adminstration_panel/users/profile/{obj.id}/change/">{obj.user}</a>')

    def user_link(self, obj):
    	return format_html(f'<a href="/go_to/the_site_adminstration_panel/auth/user/{obj.user.id}/change/">User</a>')

    actions = ['make_banned', 'make_unbanned']

    def make_banned(self, request, queryset):
        banned = queryset.update(banned=True)
        self.message_user(request, ngettext(
            '%d account was successfully marked as banned.',
            '%d accounts were successfully marked as banned.',
            banned,
        ) % banned, messages.SUCCESS)

    make_banned.short_description = "Mark selected accounts as banned"    

    def make_unbanned(self, request, queryset):
        unbanned = queryset.update(banned=False)
        self.message_user(request, ngettext(
            '%d account was successfully marked as unbanned.',
            '%d accounts were successfully marked as unbanned.',
            unbanned,
        ) % unbanned, messages.SUCCESS)

    make_unbanned.short_description = "Mark selected accounts as unbanned"

admin.site.register(Profile, ProfileAdmin)
