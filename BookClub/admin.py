from django.contrib import admin
 
# Register your models here.
from .models import Reader, Book, Dislike, Follow, Comment, Like, Review
admin.site.register(Reader)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Book)
admin.site.register(Dislike)
admin.site.register(Review)