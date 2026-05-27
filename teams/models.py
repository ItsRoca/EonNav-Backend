from django.db import models


class PokemonData(models.Model):
    pokemon_id = models.IntegerField()
    pokemon_name = models.CharField(max_length=100)
    ability = models.CharField(max_length=100)
    nature = models.CharField(max_length=100)
    move1 = models.CharField(max_length=100)
    move2 = models.CharField(max_length=100)
    move3 = models.CharField(max_length=100)
    move4 = models.CharField(max_length=100)


class Team(models.Model):
    name = models.CharField(max_length=100)
    pokemons = models.ManyToManyField(PokemonData)