from django.urls import path, include
from django.conf import settings
from . import views
from .views import *
 
 
urlpatterns = [ 
    path(r'joke/<int:pk>', JokeView.as_view(), name="joke"),
    path(r'jokes', views.JokesView, name="jokes"),
    path(r'picture/<int:pk>', PictureView.as_view(), name="picture"),
    path(r'pictures', views.PicturesView, name="pictures"),
    path(r'', views.random_view, name="random"),
    
    path('api/', JokeViewSet.as_view({'get': 'random_joke'})),
    path('api/random', JokeViewSet.as_view({'get': 'random_joke'})),
    path('api/jokes', JokeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/joke/<int:pk>', JokeViewSet.as_view({'get': 'retrieve'})),
    path('api/pictures', PictureViewSet.as_view({'get': 'list'})),
    path('api/picture/<int:pk>', PictureViewSet.as_view({'get': 'retrieve'})),
    path('api/random_picture', PictureViewSet.as_view({'get': 'random_picture'})),
]
'''path(r'', RandomDetailView.as_view(), name="random"),'''