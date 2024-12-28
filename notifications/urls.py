from django.urls import path
from .import views


urlpatterns = [

    # NotificationsPage
    path('notifications/', views.notifications, name='notifications'),
    
    #Clear notifications.
    path('clear_notifications/', views.clear_notifications, name='clear_notifications'),
]
