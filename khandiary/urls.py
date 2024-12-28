from django.urls import path
from django.contrib.auth import views as authViews 

from .import views

urlpatterns = [

    # Documentation Page
    path('documentation/', views.documentation, name='documentation'),

    # Log In Page
    path('login/', authViews.LoginView.as_view(
        template_name='khandiary/login.html'), name='login'),

    # Explore Page
    path('explore/', views.explore, name='explore'),

    # Home Page
    path('', views.index, name='index'),

    # About us Page
    path('about/', views.about, name='about'),

    # FAQ page
    path('faq/', views.faq, name='faq'),

    # Privacy Policy  Page
    path('privacy/', views.privacy, name='privacy'),

    # Terms & Conditions  Page
    path('terms/', views.terms, name='terms'),

    # Contact us Page
    path('contact/', views.contact, name='contact'),

    # Explore Page
    path('explore/', views.explore, name='explore'),

    # Search User or Entry 
    path('search_user_or_entry/<int:option>/', views.search_user_or_entry, name='search_user_or_entry'),

    # Log out page
    path('logout/', views.logout, name='logout'),
    
]
