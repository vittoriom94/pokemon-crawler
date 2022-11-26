from rest_framework import routers

from pokedex.views import PokemonViewset

app_name = "pokedex"

router = routers.DefaultRouter()
router.register(r"", PokemonViewset)

urlpatterns = router.urls