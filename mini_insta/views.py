# File: views.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The views file with a view for each page

from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import random
from .models import Profile, Photo, Post
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse
 
 
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

class PostDetailView(DetailView):
    model = Post # retrieve objects of type Post from the database
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

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

class ShowAllPostsView(ListView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
 
 
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_all_posts.html'
    context_object_name = 'profiles'

class CreatePostView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''
 
 
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.profile = profile # set the FK
 
 
        # delegate the work to the superclass method form_valid:
        response = super().form_valid(form)
    
        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
 
 
        # create and return a URL:
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('profile', kwargs={'pk':pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=pk)
        return context

class UpdateProfileView(UpdateView):
    '''A view to update an Article and save it to the database.'''
 
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
 
 
        return super().form_valid(form)
    
class UpdatePostView(UpdateView):
    '''A view to update an Article and save it to the database.'''
 
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
 
 
        return super().form_valid(form)

class DeletePostView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''
 
    template_name = "mini_insta/delete_post_form.html"
    model = Post
    context_object_name = 'post'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
 
 
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        profile = post.profile
        
        # reverse to show the article page
        return reverse('profile', kwargs={'pk':profile.pk})
    
class FollowersDetailView(DetailView):
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class FollowingDetailView(DetailView):
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class ShowFeedView(DetailView):
    '''Create a subclass of DetailView to display all followed posts.'''
 
 
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

class SearchView(ListView):
    '''Create a subclass of ListView to display all posts and profiles related to a search.'''

    template_name = 'mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in request.GET:
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=pk)
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=pk)
        context['query'] = query
        context['posts'] = Post.objects.filter(caption__icontains=query)
        context['profiles'] = Profile.objects.filter(
            username__icontains=query
        ) | Profile.objects.filter(
            display_name__icontains=query
        ) | Profile.objects.filter(
            bio_text__icontains=query
        )
        return context