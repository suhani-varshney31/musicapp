from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=24)
    notes = models.CharField(max_length=100) 

    def __str__(self):
        return self.name



class Song(models.Model):
    title = models.CharField(max_length=255)
    artists = models.TextField()  
    genre = models.CharField(max_length=100)
    album_or_movie = models.CharField(max_length=255, null=True, blank=True)
    user_rating = models.CharField(max_length=10, null=True, blank=True) 
    url = models.URLField(max_length=500, null=True, blank=True) 


    def __str__(self):
        return self.title

