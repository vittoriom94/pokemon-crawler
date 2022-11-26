import rest_framework.serializers

from pokedex.models import Pokemon, Species, Type, Ability


class SpeciesSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class TypeSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class AbilitySerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"


class PokemonSerializer(rest_framework.serializers.ModelSerializer):
    species = SpeciesSerializer()
    types = TypeSerializer(many=True)
    abilities = AbilitySerializer(many=True)

    class Meta:
        model = Pokemon
        fields = ["id", "name", "order", "description", "species", "types", "abilities"]
