"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Hopscotch API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts-urls')),
    path('stories/', include('stories.urls', namespace='stories-urls')),
    path('stories-routes/', include('stories_routes.urls', namespace='stories-routes-urls')),
    path('hopscotch/', include('hopscotch.urls', namespace='hopscotch-urls')),
    path('documentation/', schema_view)
]
