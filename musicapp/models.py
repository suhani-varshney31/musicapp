from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=24)
    notes = models.CharField(max_length=100) 
