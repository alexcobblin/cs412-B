from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Reader, Book, Comment, Dislike, Follow, Like, Review
from django.contrib.auth.mixins import LoginRequiredMixin

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
 
 
    model = Book # retrieve objects of type Profile from the database
    template_name = 'BookClub/show_all.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    '''Display the details of a single Profile.'''
    model = Book # retrieve objects of type Post from the database
    template_name = 'BookClub/show_book.html'
    context_object_name = 'book'
