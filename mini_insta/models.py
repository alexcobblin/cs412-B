# File: models.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The models file with each of our database templates

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of an Profile by some author.'''
 
 
    # data attributes of a Profile:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.username} joined {self.join_date}'
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('profile', kwargs={'pk':self.pk})
    
    def get_all_posts(self):
        '''Return all of the comments about this Profile.'''
        posts = Post.objects.filter(profile=self)
        return posts
 
class Post(models.Model):
    '''Encapsulate the idea of an Profile by some author.'''


    # data attributes of a Profile:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Post object.'''
        return f'{self.caption}'
    
    def get_all_photos(self):
        '''Return all of the photos associated with this Post.'''
        photos = Photo.objects.filter(post=self)
        return photos

class Photo(models.Model):
    '''Encapsulate the idea of an Profile by some author.'''


    # data attributes of a Profile:
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=False)
    image_url = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        return self.image_file.url

    def __str__(self):
        '''Return a string representation of this Photo object.'''
        return f'{self.image_url}'
    