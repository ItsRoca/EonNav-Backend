from rest_framework.decorators import api_view
from rest_framework.response import Response

from favorites.models import Favorite


@api_view(['GET', 'POST', 'DELETE'])
def favorites(request):

    if request.method == 'GET':
        user_id = request.GET.get('user_id')

        if not user_id:
            return Response({"error": "user_id requerido"}, status=400)

        favorites = Favorite.objects.filter(user=user_id)

        data = [
            {
                "id": f.id,
                "pokemon_name": f.pokemon_name
            }
            for f in favorites
        ]

        return Response(data)

    if request.method == 'POST':
        user_id = request.data.get("user_id")
        pokemon = request.data.get("pokemon_name")

        if not user_id or not pokemon:
            return Response({"error": "datos incompletos"}, status=400)

        # Evitar duplicados
        if Favorite.objects.filter(user=user_id, pokemon_name=pokemon).exists():
            return Response({"message": "ya existe"}, status=200)

        fav = Favorite.objects.create(
            user=user_id,
            pokemon_name=pokemon
        )

        return Response({
            "id": fav.id,
            "pokemon_name": fav.pokemon_name
        })

    if request.method == 'DELETE':
        fav_id = request.GET.get("id")

        if not fav_id:
            return Response({"error": "id requerido"}, status=400)

        try:
            fav = Favorite.objects.get(id=fav_id)
            fav.delete()
            return Response({"message": "deleted"})
        except Favorite.DoesNotExist:
            return Response({"error": "not found"}, status=404)
