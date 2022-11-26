from unittest import mock

import django.test
import pokedex.crawler
from pokedex.models import Species, Type, Ability


def mock_species_get(url, name="Species", order=1):
    return {
        "name": name,
        "order": order,
        "gender_rate": 1,
        "capture_rate": 1,
        "is_baby": True,
        "is_legendary": True,
        "is_mythical": True
    }


def mock_ability_get(url, name="Ability", language="en"):
    return {
        "name": name,
        "effect_entries": [
            {
                "effect": "Effect",
                "short_effect": "Short",
                "language": {
                    "name": language
                }
            }
        ]
    }


def mock_type_get(url, name="Type"):
    return {
        "name": name
    }


class TestImportSpecies(django.test.TestCase):
    def test_import_new(self):
        with mock.patch("pokedex.crawler.pokeapi.species_get", side_effect=lambda url: mock_species_get(url, "NewSpecies")):
            pokedex.crawler.import_species("")
        self.assertEqual(Species.objects.count(), 1)
        self.assertEqual(Species.objects.first().name, "NewSpecies")

    def test_import_multiple(self):
        with mock.patch("pokedex.crawler.pokeapi.species_get", side_effect=lambda url: mock_species_get(url, "OldSpecies", 1)):
            old = pokedex.crawler.import_species("")

        with mock.patch("pokedex.crawler.pokeapi.species_get", side_effect=lambda url: mock_species_get(url, "NewSpecies", 2)):
            new = pokedex.crawler.import_species("")
        self.assertEqual(Species.objects.count(), 2)
        self.assertEqual(old.name, "OldSpecies")
        self.assertEqual(new.name, "NewSpecies")

    def test_update(self):
        with mock.patch("pokedex.crawler.pokeapi.species_get", side_effect=lambda url: mock_species_get(url, "NewSpecies")):
            pokedex.crawler.import_species("")
            self.assertEqual(Species.objects.count(), 1)
            self.assertEqual(Species.objects.first().name, "NewSpecies")
            pokedex.crawler.import_species("")
            self.assertEqual(Species.objects.count(), 1)
            self.assertEqual(Species.objects.first().name, "NewSpecies")


class TestImportType(django.test.TestCase):
    def test_import_new(self):
        with mock.patch("pokedex.crawler.pokeapi.type_get", side_effect=lambda url: mock_type_get(url, "NewType")):
            pokedex.crawler.import_type("")
        self.assertEqual(Type.objects.count(), 1)
        self.assertEqual(Type.objects.first().name, "NewType")

    def test_import_multiple(self):
        with mock.patch("pokedex.crawler.pokeapi.type_get", side_effect=lambda url: mock_type_get(url, "OldType")):
            old = pokedex.crawler.import_type("")

        with mock.patch("pokedex.crawler.pokeapi.type_get", side_effect=lambda url: mock_type_get(url, "NewType")):
            new = pokedex.crawler.import_type("")
        self.assertEqual(Type.objects.count(), 2)
        self.assertEqual(old.name, "OldType")
        self.assertEqual(new.name, "NewType")

    def test_update(self):
        with mock.patch("pokedex.crawler.pokeapi.type_get", side_effect=lambda url: mock_type_get(url, "NewType")):
            pokedex.crawler.import_type("")
            self.assertEqual(Type.objects.count(), 1)
            self.assertEqual(Type.objects.first().name, "NewType")
            pokedex.crawler.import_type("")
            self.assertEqual(Type.objects.count(), 1)
            self.assertEqual(Type.objects.first().name, "NewType")


class TestImportAbility(django.test.TestCase):
    def test_import_new(self):
        with mock.patch("pokedex.crawler.pokeapi.ability_get", side_effect=lambda url: mock_ability_get(url, "NewEffect")):
            pokedex.crawler.import_ability("")
        self.assertEqual(Ability.objects.count(), 1)
        self.assertEqual(Ability.objects.first().name, "NewEffect")

    def test_import_multiple(self):
        with mock.patch("pokedex.crawler.pokeapi.ability_get", side_effect=lambda url: mock_ability_get(url, "OldEffect")):
            old = pokedex.crawler.import_ability("")

        with mock.patch("pokedex.crawler.pokeapi.ability_get", side_effect=lambda url: mock_ability_get(url, "NewEffect")):
            new = pokedex.crawler.import_ability("")
        self.assertEqual(Ability.objects.count(), 2)
        self.assertEqual(old.name, "OldEffect")
        self.assertEqual(new.name, "NewEffect")

    def test_update(self):
        with mock.patch("pokedex.crawler.pokeapi.ability_get", side_effect=lambda url: mock_ability_get(url, "NewEffect")):
            pokedex.crawler.import_ability("")
            self.assertEqual(Ability.objects.count(), 1)
            self.assertEqual(Ability.objects.first().name, "NewEffect")
            pokedex.crawler.import_ability("")
            self.assertEqual(Ability.objects.count(), 1)
            self.assertEqual(Ability.objects.first().name, "NewEffect")

    def test_language_not_found(self):
        with mock.patch("pokedex.crawler.pokeapi.ability_get", side_effect=lambda url: mock_ability_get(url, "NewEffect", "es")), self.assertRaises(ValueError):
            pokedex.crawler.import_ability("")