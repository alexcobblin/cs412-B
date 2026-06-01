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
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)