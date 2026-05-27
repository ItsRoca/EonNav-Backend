from django.views.decorators.csrf import csrf_exempt


# GUARDAR EQUIPO
from django.http import JsonResponse
from .models import Team, PokemonData
import json

@csrf_exempt
def save_team(request):

    if request.method == "POST":

        body = json.loads(request.body)

        team_id = body.get("id")

        # SI VIENE ID --> ACTUALIZAR
        if team_id and team_id != -1:
            try:
                team = Team.objects.get(id=team_id)
                team.name = body["name"]
                team.pokemons.clear()

            except Team.DoesNotExist:
                # Crear si no existe
                team = Team.objects.create(name=body["name"])

        # SI NO VIENE ID --> CREAR
        else:
            team = Team.objects.create(name=body["name"])

        # AÑADIR POKEMON
        for p in body["pokemons"]:
            pokemon = PokemonData.objects.create(
                pokemon_id=p["id"],
                pokemon_name=p["pokemonName"],
                ability=p["ability"],
                nature=p["nature"],
                move1=p["move1"],
                move2=p["move2"],
                move3=p["move3"],
                move4=p["move4"]
            )
            team.pokemons.add(pokemon)

        team.save()

        return JsonResponse({
            "status": "ok",
            "team_id": team.id
        })

    return JsonResponse({"error": "Use POST"})

@csrf_exempt
def create_team(request):

    team = Team.objects.create(name="Nuevo equipo")

    return JsonResponse({"id": team.id, "name": team.name})

@csrf_exempt
def get_teams(request):
    query = request.GET.get("name")

    teams = Team.objects.all()

    if query:
        teams = teams.filter(name__icontains=query)

    data = []

    for t in teams:

        pokemons = []

        for p in t.pokemons.all():
            pokemons.append({
                "id": p.pokemon_id
            })

        data.append({
            "id": t.id,
            "name": t.name,
            "pokemons": pokemons
        })

    return JsonResponse(data, safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def team_detail(request, id):

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    # GET
    if request.method == "GET":

        data = {
            "id": team.id,
            "name": team.name,
            "pokemons": []
        }

        for p in team.pokemons.all():
            data["pokemons"].append({
                "id": p.pokemon_id,
                "pokemonName": p.pokemon_name,
                "ability": p.ability,
                "nature": p.nature,
                "move1": p.move1,
                "move2": p.move2,
                "move3": p.move3,
                "move4": p.move4
            })

        return JsonResponse(data)

    # PUT
    elif request.method == "PUT":

        body = json.loads(request.body)

        team.name = body["name"]
        team.pokemons.clear()

        for p in body["pokemons"]:
            pokemon = PokemonData.objects.create(
                pokemon_id=p["id"],
                pokemon_name=p["pokemonName"],
                ability=p["ability"],
                nature=p["nature"],
                move1=p["move1"],
                move2=p["move2"],
                move3=p["move3"],
                move4=p["move4"]
            )
            team.pokemons.add(pokemon)

        team.save()

        return JsonResponse({"status": "updated"})

    # DELETE
    elif request.method == "DELETE":

        team.delete()
        return JsonResponse({"status": "deleted"})

    return JsonResponse({"error": "invalid method"}, status=400)