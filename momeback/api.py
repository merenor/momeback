from rest_framework.routers import DefaultRouter
from monsterapi.views import (PrinterViewSet, BookViewSet, OwnerViewSet,
    MonsterViewSet, MelodyViewSet, GameViewSet, CheckViewSet, RecipeViewSet,
    NameViewSet)

router = DefaultRouter()

# ROUTERS add support for automatic URL routing to django
# it is used for all ''/detail/''-requests, i.e. ''/detail/monsters/''
# lists all monster datasets, or ''detail/monsters/1/'' lists the first monster

books_router = router.register('books', BookViewSet)
# owner and printer belong to book, but we can request them individually, too
owner_router = router.register('owners', OwnerViewSet)
printers_router = router.register('printers', PrinterViewSet)

# perhaps the most important data
monsters_router = router.register('monsters', MonsterViewSet)
names_router = router.register('names', NameViewSet)

# perhaps the ugliest data
melodies_router = router.register('melodies', MelodyViewSet)

# recipes are given if a user choice is wrong
# (''the monster wants to reduce you to Möpkenbrot'') :-)
recipes_router = router.register('recipes', RecipeViewSet)

# games and checks allow a sight ''behind the scenes'' of monstermelodies
# they can be used for debugging, but also for statistical reasons
games_router = router.register('games', GameViewSet)
checks_router = router.register('checks', CheckViewSet)
