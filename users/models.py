from django.db import models
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from entries.models import Entry


# Gender choice
genders = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class Profile(models.Model):
    """User Profile"""

    # User Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=genders)
    birthday = models.DateField(null=True)

    # Profile Information
    bio = models.TextField(max_length=150, blank=True, null=True)
    country = CountryField()

    # Social Connections
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    # Status
    public = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    # Connected to user profile.
    saved_entries = models.ManyToManyField(
        Entry, blank=True, related_name="saved_entries")
    liked_entries = models.ManyToManyField(
        Entry, blank=True, related_name="liked_entries")

    # Read History  (Specially used in making custom feed.)
    read_history = models.ManyToManyField(
        Entry, blank=True, related_name="read_history")

    followers = models.ManyToManyField(
        User, blank=True, related_name="followers")

    following = models.ManyToManyField(
        User, blank=True, related_name="following")

    def entries_count(self):
        entries = Entry.objects.filter(user=self.user).count()
        return entries

    def __str__(self):
        return str(self.user)
