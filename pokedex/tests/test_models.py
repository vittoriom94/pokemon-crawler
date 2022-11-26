import django.test

from pokedex.models import Ability, Pokemon, Species, PokemonAbility, Type, PokemonType


class TestPokemonAbilityRelation(django.test.TestCase):
    def setUp(self):
        self.species = Species.objects.create(
            name="Pokemon",
            order=1,
            gender_rate=0,
            capture_rate=0,
            is_baby=True,
            is_legendary=False,
            is_mythical=False
        )

    def test_many_to_many_relation_through(self):
        ability = Ability.objects.create(name="Ability0")
        pokemon = Pokemon.objects.create(
            name="NewPokemon",
            order=1,
            species=self.species
        )

        PokemonAbility.objects.create(
            pokemon=pokemon,
            ability=ability,
            is_hidden=False,
            slot=1
        )

        self.assertEqual(pokemon.abilities.count(), 1)
        self.assertEqual(pokemon.abilities.first(), ability)

        pokemon.delete()

        self.assertEqual(PokemonAbility.objects.count(), 0)
        self.assertEqual(ability.pokemon_set.count(), 0)


class TestPokemonTypeRelation(django.test.TestCase):
    def setUp(self):
        self.species = Species.objects.create(
            name="Pokemon",
            order=1,
            gender_rate=0,
            capture_rate=0,
            is_baby=True,
            is_legendary=False,
            is_mythical=False
        )

    def test_many_to_many_relation_through(self):
        type = Type.objects.create(name="Grass")
        pokemon = Pokemon.objects.create(
            name="NewPokemon",
            order=1,
            species=self.species
        )

        PokemonType.objects.create(
            pokemon=pokemon,
            type=type,
            slot=1
        )

        self.assertEqual(pokemon.types.count(), 1)
        self.assertEqual(pokemon.types.first(), type)

        pokemon.delete()

        self.assertEqual(PokemonType.objects.count(), 0)
        self.assertEqual(type.pokemon_set.count(), 0)


class TestPokemonDescription(django.test.TestCase):
    def setUp(self) -> None:
        self.species = Species.objects.create(
            name="Pokemon",
            order=1,
            gender_rate=0,
            capture_rate=0,
            is_baby=True,
            is_legendary=False,
            is_mythical=False
        )
        self.pokemon = Pokemon.objects.create(
            name="NewPokemon",
            order=1,
            species=self.species
        )

    def test_no_types(self):
        self.assertEqual(self.pokemon.description, "Pokèmon of the species Pokemon. It doesn't have a type.")

    def test_one_type(self):
        type = Type.objects.create(name="Grass")
        PokemonType.objects.create(
            pokemon=self.pokemon,
            type=type,
            slot=1
        )

        self.assertEqual(self.pokemon.description, "Pokèmon of the species Pokemon. It belongs to types Grass.")
        type.delete()

    def test_multiple_types(self):
        type_1 = Type.objects.create(name="Grass")
        PokemonType.objects.create(
            pokemon=self.pokemon,
            type=type_1,
            slot=1
        )

        type_2 = Type.objects.create(name="Fire")
        PokemonType.objects.create(
            pokemon=self.pokemon,
            type=type_2,
            slot=2
        )

        self.assertEqual(self.pokemon.description, "Pokèmon of the species Pokemon. It belongs to types Grass, Fire.")
        type_1.delete()
        type_2.delete()