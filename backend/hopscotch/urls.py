from django.urls import path
from .views import HopscotchView

app_name = 'hopscotch-urls'

urlpatterns = [
    path('your-hopscotch/', HopscotchView.as_view()),

]