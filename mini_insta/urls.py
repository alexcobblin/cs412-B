from django.urls import path
from .views import ShowAllView, ProfileDetailView, RandomProfileView
from django.conf import settings
from . import views
from django.conf.urls.static import static
 
 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomProfileView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name='show_all'), # generic class-based view
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)