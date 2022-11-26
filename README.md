# Pokemon Crawler

## Instructions

* `docker-compose up`

Tests can be run either locally or in the docker instances with the default django testing framework:
* `python manage.py test`


## Endpoint

User http://localhost:8000/pokedex/ to check out the imported pokemon.

## Crawler

Crawling will be done at two times:
* At startup, when the database is empty (give it some time!).
* Every 24 hours, so that pokemon can be updated

## Database

![Schema](https://i.imgur.com/9XLa5kt_d.webp?maxwidth=760&fidelity=grand)

As per requirements, each Pokemon will have data crawled from the API.

The choices were:
- name
- order
- species
- abilities
- type

A description is dynamically added on visualization.

## Design choices
Due to Pokeapi requiring to call an endpoint for each pokemon, ability, type and species, this project shows each pokemon
completed with all its data, so that it is not necessary to query Pokeapi multiple times and this app can be used to see
all the available pokemon and their properties.

Django Rest framework has been used, so it would be easy and fast to add features, like ordering and searching.

Crawling is done once at startup, and every 24 hours. This allows to update the database with a good 
precision in case new pokemon or abilities are discovered.
The crawling could be sped up by using multiple workers. Because Pokeapi kindly asks to not overload the server,
crawling happens synchronously.

As celery is a separate worker, there is no risk of overloading the main server, so it is possible to run the import task at the preferred time (possibly ask Prof. Oak).

Due to time constraint, the project is not production ready, as it can be seen from the settings.

## Test

Testing has been done with TDD in mind, by testing the critical points of the project.

The aim of those tests is to verify the interaction between the different models, and to ensure that
the schema presented by Pokeapi is correctly parsed.

## Further considerations

- Importing data could be improved by using a ThreadPoolExecutor, as the crawling task is mainly I/O bound.
- The visualization can be improved by using the through models.
- The crawling module is not completely tested due to time constraint, this should be the first area of improvement.
- Deployment should start from using environment variables, instead of hard coded values for stuff like DB and Redis connections.
- Logging and error handling can be improved
