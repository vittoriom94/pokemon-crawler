import logging

from celery import signals, shared_task
import pokedex.crawler
from pokedex.models import Pokemon


@shared_task
def refresh_pokedex():
    logging.info("Refreshing pokedex")
    pokedex.crawler.crawl()
    logging.info("Refresh done")


@signals.worker_ready.connect
def first_import(sender, **k):
    pokemon_count = Pokemon.objects.count()
    if not pokemon_count:
        logging.info("No pokemon found in DB, starting import.")
        pokedex.crawler.crawl()
        logging.info("Import done")

