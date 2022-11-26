import logging

from pokedex import pokeapi
from pokedex.models import Pokemon, Species, Ability, Type, PokemonType, PokemonAbility


def crawl():
    import_abilities()
    import_types()
    import_pokedex()


def import_pokedex():
    """
    Imports the full list of pokemon into the database
    """
    pokemons = pokeapi.pokemon_list()
    for pokemon in pokemons:
        import_pokemon(pokemon["url"])


def import_pokemon(pokemon_url: str):
    """
    Import one pokemon in the database
    """
    pokemon = pokeapi.pokemon_get(pokemon_url)
    if pokemon["name"] == "bulbasaur":
        print("found")
    if Pokemon.objects.filter(name=pokemon["name"]).exists():
        update_pokemon(pokemon)
    else:
        create_pokemon(pokemon)


def import_species(species_url: str):
    species = pokeapi.species_get(species_url)
    obj, created = Species.objects.update_or_create(
        name=species["name"],
        defaults={
            "order": species["order"],
            "gender_rate": species["gender_rate"],
            "capture_rate": species["capture_rate"],
            "is_baby": species["is_baby"],
            "is_legendary": species["is_legendary"],
            "is_mythical": species["is_mythical"]
        }
    )
    return obj


def import_abilities():
    abilities = pokeapi.ability_list()
    for ability in abilities:
        import_ability(ability["url"])


def import_types():
    types = pokeapi.type_list()
    for type in types:
        import_type(type["url"])


def import_ability(ability_url: str):
    ability = pokeapi.ability_get(ability_url)
    logging.debug(f"Imported ability {ability_url}")
    effect = find_english_ability_description(ability["effect_entries"])

    obj, created = Ability.objects.update_or_create(
        name=ability["name"],
        defaults={
            "effect": effect["effect"],
            "short_effect": effect["short_effect"]
        }
    )
    return obj


def find_english_ability_description(effect_entries: list) -> dict:
    if not effect_entries:
        return {
            "effect": None,
            "short_effect": None
        }
    for entry in effect_entries:
        if entry["language"]["name"] == "en":
            return entry
    raise ValueError("Could not find 'en' entry in languages.")


def import_type(type_url: str):
    type = pokeapi.type_get(type_url)

    obj, created = Type.objects.update_or_create(
        name=type["name"]
    )
    return obj


def create_pokemon(pokemon: dict):
    pokemon_instance = Pokemon.objects.create(
        name=pokemon["name"],
        order=pokemon["order"],
        species=import_species(pokemon["species"]["url"])
    )

    create_pokemon_types(pokemon_instance, pokemon)
    create_pokemon_abilities(pokemon_instance, pokemon)


def update_pokemon(pokemon: dict):
    pokemon_instance = Pokemon.objects.get(name=pokemon["name"])
    pokemon_instance.order = pokemon["order"]
    pokemon_instance.species = import_species(pokemon["species"]["url"])
    pokemon_instance.save()

    pokemon_instance.types.clear()
    pokemon_instance.abilities.clear()

    create_pokemon_types(pokemon_instance, pokemon)
    create_pokemon_abilities(pokemon_instance, pokemon)


def create_pokemon_types(pokemon_instance: Pokemon, pokemon_data: dict):
    for type in pokemon_data["types"]:
        PokemonType.objects.create(
            pokemon=pokemon_instance,
            type=Type.objects.get(name=type["type"]["name"]),
            slot=type["slot"]
        )


def create_pokemon_abilities(pokemon_instance: Pokemon, pokemon_data: dict):
    for ability in pokemon_data["abilities"]:
        PokemonAbility.objects.create(
            pokemon=pokemon_instance,
            ability=Ability.objects.get(name=ability["ability"]["name"]),
            is_hidden=ability["is_hidden"],
            slot=ability["slot"]
        )
