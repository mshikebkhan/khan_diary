from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authViews 
from django.conf import settings

import admin_interface
from .import views

if settings.CONSTRUCTION == False:

    urlpatterns = [

        # Admin portal url config.
        path('go_to/the_site_adminstration_panel/', admin.site.urls),

        # Diarygram url config.
        path('', include(('khandiary.urls', 'khandiary'), namespace='khandiary')),

        # Entries url config.
        path('', include(('entries.urls', 'entries'), namespace='entries')),

        # Notifications url config.
        path('', include(('notifications.urls', 'notifications'), namespace='notifications')),

        # Users url config.
        path('', include(('users.urls', 'users'), namespace='users')),

        # Forgot password reset
        path('password_reset/', authViews.PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html'), name='password_reset'),
        path('password_reset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('password_reset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('password_reset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    ]
else:
    urlpatterns = [path('', views.construction, name='construction'),]


# Page not found
handler404 = "website.views.page_not_found_view"

# Admin portal config.

# default: "Django Administration"
admin.site.site_header = 'Khan Diary Adminstration'
admin.site.index_title = 'Site Administration'
admin.site.site_title = "Khan Diary - Admin"
