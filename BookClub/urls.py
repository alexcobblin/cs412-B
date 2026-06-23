# File: urls.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The urls file with a view for each page

from django.urls import path
from BookClub.views import ShowAllView, BookDetailView
from django.conf import settings
from django.conf.urls.static import static
 
 
urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all"),
    path('book/<int:pk>', BookDetailView.as_view(), name="book"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)