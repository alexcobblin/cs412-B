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
    def get_all_followers(self):
        '''Return all of the comments about this Profile.'''
        followers = list(Follow.objects.filter(profile=self))
        return followers
    def get_num_followers(self):
        return len(self.get_all_followers())
    def get_following(self):
        '''Return all of the comments about this Profile.'''
        following = list(Follow.objects.filter(follower_profile=self))
        return following
    def get_num_following(self):
        return len(self.get_following())
    def get_post_feed(self):
        return Post.objects.filter(
            profile__in=Profile.objects.filter(
                profile__follower_profile=self)).order_by('-timestamp')
 
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
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('post', kwargs={'pk':self.pk})
    def get_all_comments(self):
        '''Return all of the comments about this Profile.'''
        comments = Comment.objects.filter(post=self)
        return comments
    def get_likes(self):
        '''Return all of the likes associated with this Post.'''
        likes = Like.objects.filter(post=self)
        return likes
    def stylish_likes(self):
        likes = self.get_likes()
        count = likes.count()

        if count == 0:
            return "No likes yet"
        first_name = likes[0].profile.display_name

        if count == 1:
            return f"{first_name} liked this post"

        return f"{first_name} and {count - 1} others liked this post"

class Photo(models.Model):
    '''Encapsulate the idea of an Photo by some profile.'''


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

class Follow(models.Model):
    '''Encapsulate the idea of a follow.'''

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'

class Comment(models.Model):
    '''Encapsulate the idea of a comment.'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'

class Like(models.Model):
    '''Encapsulate the idea of a like.'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Like object.'''
        return f'{self.profile.display_name} liked {self.post}'