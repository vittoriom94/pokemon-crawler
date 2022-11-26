import rest_framework.viewsets

from pokedex.models import Pokemon
from pokedex.serializers import PokemonSerializer


class PokemonViewset(rest_framework.viewsets.ReadOnlyModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
