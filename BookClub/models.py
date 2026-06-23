# File: models.py
# Author: Alex Cobb (alcobb@bu.edu), 6/16/2006
# Description: The models file with each of our database templates

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator #for star rating

# Create your models here.
class Reader(models.Model):
    '''Encapsulate the idea of an Reader.'''
 
 
    # data attributes of a Reader:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    reader_image_url = models.TextField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        '''Return a string representation of this Reader object.'''
        return f'{self.username} joined {self.join_date}'
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('reader', kwargs={'pk':self.pk})
    
    def get_all_comments(self):
        '''Return all of the comments about this Reader.'''
        comments = Comment.objects.filter(reader=self)
        return comments
    
    def get_all_followers(self):
        '''Return all of the comments about this Reader.'''
        followers = list(Follow.objects.filter(reader=self))
        return followers
    
    def get_num_followers(self):
        return len(self.get_all_followers())
    def get_following(self):
        '''Return all of the comments about this Reader.'''
        following = list(Follow.objects.filter(follower_reader=self))
        return following
    
    def get_num_following(self):
        return len(self.get_following())
 
class Book(models.Model):
    '''Encapsulate the idea of an Book by some author.'''


    # data attributes of a Reader:
    image_file = models.ImageField(blank=False)
    book_name = models.TextField(blank=False)
    author = models.TextField(blank=False)
    description = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Book object.'''
        return f'{self.book_name}'
    
    def get_all_comments(self):
        '''Return all of the comments associated with this Post.'''
        comments = Comment.objects.filter(book=self).order_by('page_num')
        print(comments)
        com_list = list(comments)
        for i in com_list:
            replies = list(i.get_replies())
            for j in replies:
                print(j)
                com_list.remove(j)
                com_list.insert((com_list.index(j.reply) + 1), j)
        return comments
    def get_all_reviews(self):
        '''Return all of the reviews associated with this Post.'''
        reviews = Review.objects.filter(book=self)
        return reviews
    def stylish_reviews(self):
        reviews = self.get_all_reviews()
        count = reviews.count()
        if count > 0:
            temp = 0
            for i in reviews:
                temp += i.stars
            avg = temp / count

            return ""+str(round(avg, 2))+f" - {count} reviews"
        return "No reviews"
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('book', kwargs={'pk':self.pk})
    def unique_page_nums(self):
        nums = []
        for i in Comment.objects.filter(book=self):
            if i.page_num not in nums:
                nums.append(i.page_num)
        return nums

class Follow(models.Model):
    '''Encapsulate the idea of a follow.'''

    reader = models.ForeignKey("Reader", on_delete=models.CASCADE, related_name="reader")
    follower_reader = models.ForeignKey("Reader", on_delete=models.CASCADE, related_name="follower_reader")
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        '''Return a string representation of this Reader object.'''
        return f'{self.follower_reader.display_name} follows {self.reader.display_name}'

class Comment(models.Model):
    '''Encapsulate the idea of a comment.'''
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)

    # I wanted people to be able to optionally reply to comments
    # The reply variable is optional and self referential
    reply = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)
    page_num = models.IntegerField(blank=False)

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'
    def get_likes(self):
        '''Return all of the likes associated with this Post.'''
        likes = Like.objects.filter(comment=self)
        return likes
    def stylish_likes(self):
        likes = self.get_likes()
        count = likes.count()

        return f"👍 {count}"
    def get_dislikes(self):
        '''Return all of the likes associated with this Post.'''
        dislike = Dislike.objects.filter(comment=self)
        return dislike
    def stylish_dislikes(self):
        dislike = self.get_dislikes()
        count = dislike.count()

        return f"👎 {count}"
    def get_replies(self):
        comments = Comment.objects.filter(reply=self)
        return comments

class Like(models.Model):
    '''Encapsulate the idea of a like.'''
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    comment = models.ForeignKey("comment", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Like object.'''
        return f'{self.reader.display_name} liked {self.comment}'
    
class Dislike(models.Model):
    '''Encapsulate the idea of a like.'''
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Dislike object.'''
        return f'{self.reader.display_name} disliked {self.comment}'

class Review(models.Model):
    '''Encapsulate the idea of a review.'''
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this Review object.'''
        return f'{self.text}'