from django.db import models
from django.forms import ModelForm

# Create your models here.

class Blurb(models.Model):
    description = models.CharField(max_length=200)

class BlurbForm(ModelForm):
    class Meta:
        model = Blurb
        fields = ['description']