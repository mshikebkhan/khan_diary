from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.template import Context

from notifications.models import Notification

# Mood choice
moods = [
    ('great', "Great mood"),
    ('good', "Good mood"),
    ('usual', "Usual mood"),
    ('bad', "Bad mood"),
    ('terrible', "Terrible mood")
]


class Entry(models.Model):
    """ The Diary Entry """

    # Attached with the user.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Main Content
    content = models.TextField(max_length=750)

    # User's mood while writing.
    mood = models.CharField(max_length=30, choices=moods)

    # Meta Info
    likes = models.PositiveIntegerField(default=0)
    reads = models.PositiveIntegerField(default=0)
    reported = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    # Date
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # The private entry must not be shown on admin panel for users privacy.

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"


    def user_add_entry(sender, instance, created, *args, **kwargs):
        """Add notification for followers if user add entry."""
        if created:
            entry = instance
            preview = entry.content[:70]
            sender = entry.user

            for follower in entry.user.profile.followers.all():
                notify = Notification(entry=entry, sender=sender, user=follower, preview=preview ,notification_type=1)
                notify.save()

    def user_delete_entry(sender, instance, *args, **kwargs):
        """Remove notification for followers if user deleted entry."""
        entry = instance
        preview = entry.content[:70]
        sender = entry.user
        for follower in entry.user.profile.followers.all():
            notify = Notification.objects.filter(entry=entry, sender=sender, user=follower, preview=preview ,notification_type=1)
            notify.delete()

    def __str__(self):
        return self.content[:50]

#Entry notify.
post_save.connect(Entry.user_add_entry, sender=Entry)
post_delete.connect(Entry.user_delete_entry, sender=Entry)