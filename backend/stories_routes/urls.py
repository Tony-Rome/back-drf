from django.urls import path
from .views import StoriesRoutesView, StoriesRoutesListView, OrderByRouteView

app_name = 'stories-routes-urls'

urlpatterns = [
    path('your-stories-routes/', StoriesRoutesView.as_view()),
    path('all-stories-routes/', StoriesRoutesListView.as_view()),
    path('your-order-routes/', OrderByRouteView.as_view()),
]