# File: urls.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The urls file with a view for each page

from django.urls import path
from .views import *
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
 
 
urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all"),
    path('random', RandomProfileView.as_view(), name='random'),
    
    # Other users' profiles
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/followers', FollowersDetailView.as_view(), name='followers'),
    path('profile/<int:pk>/following', FollowingDetailView.as_view(), name='following'),
    
    # User's profile
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('profile', MyProfileView.as_view(), name='my_profile'),
    path('profile/feed', ShowFeedView.as_view(), name='feed'),
    path('profile/search', SearchView.as_view(), name='search'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),
    
    # Posts
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    
    # Likes and follows
    path('profile/<int:pk>/follow', FollowView.as_view(), name='follow'),
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name='delete_follow'),
    path('post/<int:pk>/like', LikePostView.as_view(), name='like'),
    path('post/<int:pk>/delete_like', DeleteLikeView.as_view(), name='delete_like'),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)