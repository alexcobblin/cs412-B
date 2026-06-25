# File: urls.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The urls file with a view for each page

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
 
 
urlpatterns = [
    path('', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book'),
    path('book/add/', views.BookSearchView.as_view(), name='add_book'),
    path('book/<int:book_pk>/comment/', views.CreateCommentView.as_view(), name='create_comment'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('book/<int:book_pk>/review/', views.CreateReviewView.as_view(), name='create_review'),
    path('reader/<int:pk>/', views.ReaderDetailView.as_view(), name='reader'),
    path('reader/<int:pk>/update/', views.UpdateReaderView.as_view(), name='update_reader'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('review/<int:pk>/edit/', views.EditReviewView.as_view(), name='edit_review'),
    path('review/<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete_review'),
    path('reader/<int:pk>/', views.ReaderDetailView.as_view(), name='reader'),
    path('comment/<int:pk>/like/', views.LikeCommentView.as_view(), name='like_comment'),
    path('comment/<int:pk>/dislike/', views.DislikeCommentView.as_view(), name='dislike_comment'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)