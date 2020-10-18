from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Photo(models.Model):
    img_url = models.TextField(max_length=2083)
    user = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.pk}'

class Album(models.Model):
    name = models.CharField(max_length=50, choices=[('HAPPINESS', 'HAPPINESS'), ('SAD', 'SAD'), ('NOSTALGIA', 'NOSTALGIA'), ('LONGING', 'LONGING')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photos = models.ManyToManyField(Photo)

    def __str__(self):
        return f'Album {self.name}; belongs to {self.user.first_name}'

class FaceToUser(models.Model):
    ExternalImageId = models.CharField(max_length=200)
    FaceId = models.CharField(max_length=200)
    user = models.ManyToManyField(User)