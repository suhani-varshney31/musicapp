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
from musicapp.views import StudentApi,LoginAPI,SignupAPI,SearchSongAPI,UploadSongsCSVAPI,RecommendSongsAPI,AddFavoriteSongAPI,GetNextSongAPI


urlpatterns = [
    path('student/', StudentApi.as_view()),
    path('login/', LoginAPI.as_view()),
    path('admin/', admin.site.urls),
    path('signup/', SignupAPI.as_view()),
    path('upload-songs-csv/', UploadSongsCSVAPI.as_view(), name='upload-songs-csv'),
    path('search-song/', SearchSongAPI.as_view(), name='search-song'), 
    path('recommend/', RecommendSongsAPI.as_view(), name='recommend-songs-api'),
    path('add_favorite/', AddFavoriteSongAPI.as_view(), name='add-favorite-song-api'),
    path('next_song/', GetNextSongAPI.as_view(), name='get-next-song-api'),
    
   
]
