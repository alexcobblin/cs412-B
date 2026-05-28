# File: models.py
# Author: Alex Cobb (alcobb@bu.edu), 5/28/2006
# Description: The models file with each of our database templates

from django.db import models

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
 