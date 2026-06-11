from django.db import models

# Create your models here.
class Joke(models.Model):
    '''Encapsulate the idea of an Profile by some author.'''


    # data attributes of a Profile:
    text = models.TextField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def get_all():
        return Joke.objects.all()
    

class Picture(models.Model):
    '''Encapsulate the idea of an Profile by some author.'''


    # data attributes of a Profile:
    name = models.TextField(blank=False)
    image_url = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def get_all():
        return Picture.objects.all()

