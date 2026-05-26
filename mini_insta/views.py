from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView
import random
 
 
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
 
 
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_all.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
 
 
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class RandomProfileView(DetailView):
    '''Show the details for one article.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
 
 
    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''
 
 
        all_profiles = Profile.objects.all()
        return random.choice(all_profiles)