from django.urls import path
from .import views


urlpatterns = [

    # All Entries Page
    path('entries/', views.entries, name='login-to-entries'),

    # All Entries Page
    path('<str:user>/entries/', views.entries, name='entries'),
    
    # Explore User Entries
    path('<str:user>/search_entry/',
         views.search_user_entry, name='search_user_entry'),

    # +1 Read to Entry
    path('add_read/<int:entry_id>/', views.add_read),

    # Add New Entry
    path('new_entry/', views.add_entry, name='new_entry'),

    # Entry Detailed Page
    path('entry/<int:entry_id>/', views.entry, name='entry'),
    
    # Edit Entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

    # Like Entry
    path('like_entry/<int:entry_id>/', views.like_entry),

    # Save Entry
    path('save_entry/<int:entry_id>/', views.save_entry),

    # Delete Entry (With JS)
    path('delete_entry/<int:entry_id>/', views.delete_entry),

    # Report Entry
    path('report_entry/<int:entry_id>/', views.report_entry),

    # Explore by mood Page
    path('mood/<str:mood>/', views.mood, name='mood'),

    # Explore by mood Page (For a specific user entries)
    path('mood/<str:mood>/<str:user>/', views.mood, name='user-mood'),
    
    # Most Liked Entries Page
    path('most_liked_entries/', views.most_liked_entries, name='most_liked_entries'),

    # Most Viewed Entries Page
    path('most_viewed_entries/', views.most_viewed_entries, name='most_viewed_entries'),

    # Saved Entries Page
    path('saved_entries/', views.saved_entries, name='saved_entries'),

    # Liked Entries Page
    path('liked_entries/', views.liked_entries, name='liked_entries'),

    # Read History Page
    path('read_history/', views.read_history, name='read_history'),

    # Clear Read History Page
    path('clear_read_history/', views.clear_read_history, name='clear_read_history'),
    


]
