from django.urls import path, include
from django.conf import settings
from . import views
from .views import *
 
router = routers.DefaultRouter()
router.register(r"rest-pictures", PictureViewSet)
router.register(r"rest-jokes", JokeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
 
urlpatterns = [ 
    path(r'joke/<int:pk>', JokeView.as_view(), name="joke"),
    path(r'jokes', views.JokesView, name="jokes"),
    path(r'picture/<int:pk>', PictureView.as_view(), name="picture"),
    path(r'pictures', views.PicturesView, name="pictures"),
    path(r'', views.random_view, name="random"),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
'''path(r'', RandomDetailView.as_view(), name="random"),'''