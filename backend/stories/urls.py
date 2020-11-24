from django.urls import path
from .views import StoriesView, StoriesListView

app_name = 'stories-urls'

urlpatterns = [
    path('your-stories/', StoriesView.as_view()),
    path('all-stories/', StoriesListView.as_view()),
]