import django.core.validators
from django.db import models


class Ability(models.Model):
    name = models.CharField(max_length=50, unique=True)
    effect = models.TextField(null=True)
    short_effect = models.TextField(null=True)


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.IntegerField()
    gender_rate = models.IntegerField()
    capture_rate = models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])
    is_baby = models.BooleanField()
    is_legendary = models.BooleanField()
    is_mythical = models.BooleanField()


class Pokemon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.IntegerField()
    abilities = models.ManyToManyField(Ability, through='PokemonAbility')
    types = models.ManyToManyField(Type, through='PokemonType')
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    @property
    def description(self):
        type_str = "It doesn't have a type." if not self.types.count() else f"It belongs to types {', '.join((str(elem) for elem in self.types.all()))}."
        return f"Pokèmon of the species {self.species.name}. {type_str}"


class PokemonAbility(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    is_hidden = models.BooleanField()
    slot = models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])


class PokemonType(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    slot = models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])
