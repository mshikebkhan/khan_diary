from django.shortcuts import render, redirect
from .models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def count_notifications(request):
    """ Show unread notifications count on navbar. """
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

    return {'count_notifications':count_notifications}
    

@login_required
def notifications(request):
    """ Show Notifications """
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date_created')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    notifications_count = notifications.count()

    context = {
    'notifications': notifications, 'notifications_count': notifications_count,
    }

    return render(request, 'notifications/notifications.html', context)


@login_required
def clear_notifications(request):
    """Clear all notifications at once """
    if request.method == "POST":
        user = request.user
        notifications = Notification.objects.filter(user=user, is_seen=True)
        notifications.delete()
        messages.success(request, f'All notifications has been cleared successfully.')
        return redirect('notifications:notifications')
    else:
        Http404    


