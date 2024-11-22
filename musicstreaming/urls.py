"""
URL configuration for musicstreaming project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from musicapp.views import StudentApi,LoginAPI,SignupAPI,PlaySongAPI 

urlpatterns = [
    path('student/', StudentApi.as_view()),
    path('login/', LoginAPI.as_view()),
    path('admin/', admin.site.urls),
    path('signup/', SignupAPI.as_view()),
    path('play/', PlaySongAPI.as_view()),
    path('play/<int:song_id>/', PlaySongAPI.as_view(), name='play-song'),
]
