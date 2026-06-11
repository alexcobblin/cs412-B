from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Joke, Picture
import random
from rest_framework import routers, serializers, viewsets

# Create your views here.

class JokeView(DetailView):
    model = Joke
    context_object_name = 'joke'
    template_name = 'dadjokes/joke.html'

def JokesView(request):
    context = {'jokes': Joke.get_all()}
    template_name = 'dadjokes/jokes.html'

    return render(request, template_name, context)


class PictureView(DetailView):
    model = Picture
    context_object_name = 'picture'
    template_name = 'dadjokes/picture.html'

def PicturesView(request):
    context = {'pictures' : Picture.get_all()}
    template_name = 'dadjokes/pictures.html'

    return render(request, template_name, context)


def random_view(request):
    # Calling the custom class method
    context = {
        'joke': random.choice(Joke.get_all()),
        'picture': random.choice(Picture.get_all())
        }
    
    return render(request, 'dadjokes/random.html', context)

class JokeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Joke
        fields = ["text", "name", "timestamp"]


# ViewSets define the view behavior.
class JokeViewSet(viewsets.ModelViewSet):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture
        fields = ["image_url", "name", "timestamp"]


# ViewSets define the view behavior.
class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer