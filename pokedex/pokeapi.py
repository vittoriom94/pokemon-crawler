import requests


def pokemon_list() -> list[dict[str, str]]:
    """
    Return the complete list of pokemon available in format
    [ {name: "name", url: "url"}, ... ]
    """
    pokemons = []

    response = requests.get("https://pokeapi.co/api/v2/pokemon")
    response.raise_for_status()
    pokemons.extend(response.json()["results"])
    while response.json()["next"]:
        response = requests.get(response.json()["next"])
        response.raise_for_status()
        pokemons.extend(response.json()["results"])
    return pokemons


def ability_list() -> list[dict[str, str]]:
    """
    Return the complete list of abilities available in format
    [ {name: "name", url: "url"}, ... ]
    """
    abilities = []

    response = requests.get("https://pokeapi.co/api/v2/ability")
    response.raise_for_status()
    abilities.extend(response.json()["results"])
    while response.json()["next"]:
        response = requests.get(response.json()["next"])
        response.raise_for_status()
        abilities.extend(response.json()["results"])
    return abilities


def type_list() -> list[dict[str, str]]:
    """
    Return the complete list of abilities available in format
    [ {name: "name", url: "url"}, ... ]
    """
    types = []

    response = requests.get("https://pokeapi.co/api/v2/type")
    response.raise_for_status()
    types.extend(response.json()["results"])
    while response.json()["next"]:
        response = requests.get(response.json()["next"])
        response.raise_for_status()
        types.extend(response.json()["results"])
    return types


def pokemon_get(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def species_get(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def type_get(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def ability_get(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

