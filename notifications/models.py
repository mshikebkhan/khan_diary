from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    """Display notifications."""
    NOTIFICATION_TYPES = ((1,'Add Entry'),(2,'Like Entry'),(3,'Follow User'))

    entry = models.ForeignKey('entries.Entry', on_delete=models.CASCADE, related_name="noti_entry", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    preview = models.CharField(max_length=100, blank=True)
    is_seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
