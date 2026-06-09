# File: views.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The views file with a view for each page

from django.shortcuts import render, redirect
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import random
from .models import Profile, Photo, Post
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Follow, Like
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
 
 
class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''A custom mixin that requires login and provides a helper
      to retrieve the logged-in user's Profile.'''
    def get_login_url(self):
        return reverse('login')
    
    def get_logged_in_profile(self):
        return Profile.objects.get(user=self.request.user)

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
 
 
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_all.html'
    context_object_name = 'profiles'

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
 
        return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(DetailView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
 
 
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.get(user=self.request.user)
            context['logged_in_profile'] = logged_in_profile
            context['is_following'] = Follow.objects.filter(
                profile=self.object,
                follower_profile=logged_in_profile
            ).exists()
        return context

class PostDetailView(DetailView):
    '''Display the details of a single Profile.'''
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

class CreatePostView(CustomLoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''
 
 
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_login_url(self):
        return reverse('login')

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        profile = self.get_logged_in_profile()
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
        # call reverse to generate the URL for this Article
        return reverse('profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.get_logged_in_profile()
        context['profile'] = self.get_logged_in_profile()
        return context

class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    '''A view to update an Article and save it to the database.'''
 
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
    def get_object(self):
        return self.get_logged_in_profile()

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
 
 
        return super().form_valid(form)
    
class UpdatePostView(CustomLoginRequiredMixin, UpdateView):
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

class DeletePostView(CustomLoginRequiredMixin, DeleteView):
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
    '''Display all Profiles that follow a given Profile.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class FollowingDetailView(DetailView):
    '''Display all Profiles that a given Profile is following.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class ShowFeedView(CustomLoginRequiredMixin, DetailView):
    '''Create a subclass of DetailView to display all followed posts.'''
 
 
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.get_logged_in_profile()

class SearchView(CustomLoginRequiredMixin, ListView):
    '''Create a subclass of ListView to display all posts and profiles related to a search.'''

    template_name = 'mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in request.GET:
            profile = self.get_logged_in_profile()
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        context['profile'] = self.get_logged_in_profile()
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

class MyProfileView(CustomLoginRequiredMixin, DetailView):
    '''Display the profile page of the currently logged-in user.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.get_logged_in_profile()
    

class FollowView(CustomLoginRequiredMixin, TemplateView):
    '''Handle a follow action from the logged-in user toward another Profile.'''
    def dispatch(self, request, *args, **kwargs):
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        if my_profile != other_profile:
            Follow.objects.get_or_create(profile=other_profile, follower_profile=my_profile)
        return redirect('profile', pk=other_profile.pk)

class DeleteFollowView(CustomLoginRequiredMixin, TemplateView):
    '''Handle an unfollow action from the logged-in user toward another Profile.'''
    def dispatch(self, request, *args, **kwargs):
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        Follow.objects.filter(profile=other_profile, follower_profile=my_profile).delete()
        return redirect('profile', pk=other_profile.pk)

class LikePostView(CustomLoginRequiredMixin, TemplateView):
    '''Handle a like action from the logged-in user on a Post.'''
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        if post.profile != my_profile:
            Like.objects.get_or_create(post=post, profile=my_profile)
        return redirect('post', pk=post.pk)

class DeleteLikeView(CustomLoginRequiredMixin, TemplateView):
    '''Handle an unlike action from the logged-in user on a Post.'''
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        Like.objects.filter(post=post, profile=my_profile).delete()
        return redirect('post', pk=post.pk)


class CreateProfileView(CreateView):
    '''Display and process two forms simultaneously to create
      a new Django User and associated Profile.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('my_profile')