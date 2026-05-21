from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    pokemon_name = models.CharField(max_length=100)
    user = models.IntegerField()