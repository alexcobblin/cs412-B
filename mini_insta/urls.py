# File: urls.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The urls file with a view for each page

from django.urls import path
from .views import *
from django.conf import settings
from . import views
from django.conf.urls.static import static
 
 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name="show_all"),
    path('random', RandomProfileView.as_view(), name='random'), # generic class-based view
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('profile/<int:pk>/followers', FollowersDetailView.as_view(), name='followers'),
    path('profile/<int:pk>/following', FollowingDetailView.as_view(), name='following'),
    path('profile/<int:pk>/feed', ShowFeedView.as_view(), name='feed'),
    path('profile/<int:pk>/search', SearchView.as_view(), name='search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)