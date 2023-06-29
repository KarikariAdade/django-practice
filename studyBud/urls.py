"""
URL configuration for studyBud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home.html, name='home.html')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home.html')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


    Routes go here
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # Include the url file in the base app
    path('api/', include('base.api.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
