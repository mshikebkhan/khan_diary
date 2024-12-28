from django.urls import path

from .import views


urlpatterns = [

    # Sign up Page
    path('signup/', views.signup, name='signup'),
    
    # Profile Page
    path('profile/', views.profile, name='login-to-profile'),

    # Profile Page
    path('<str:user>/profile/', views.profile, name='profile'),

    # Follow User
    path('follow_user/<int:user_id>/', views.follow_user),

    # Followers Page
    path('<str:user>/followers/', views.followers, name='followers'),

    # Following Page
    path('<str:user>/following/', views.following, name='following'),

    # Most Popular Users Page
    path('most_popular_users/', views.most_popular_users, name='most_popular_users'),

    # Settings Page / Edit profile
    path('settings/edit-profile/', views.edit_profile, name='edit-profile'),

    # Settings Page / Account
    path('settings/account/',
         views.account, name='account'),

    # Change Password Page
    path('change_password/', views.change_password, name='change_password'),

    # Security Checkup Page
    path('security_checkup/', views.security_checkup, name='security_checkup'),

    # Account privacy setting
    path('account_privacy_setting/', views.account_privacy_setting, name='account_privacy_setting'),


]
