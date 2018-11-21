from rest_framework.routers import DefaultRouter
from monsterapi.views import PrinterViewSet, BookViewSet, OwnerViewSet, MonsterViewSet, MelodyViewSet
from rest_framework_extensions.routers import NestedRouterMixin

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()

books_router = router.register('books', BookViewSet)
books_router.register(
    'printer', PrinterViewSet,
    base_name='book-printer',
    parents_query_lookups=['book'])
books_router.register(
    'owner', OwnerViewSet,
    base_name='book-owner',
    parents_query_lookups=['book'])

printers_router = router.register('printers', PrinterViewSet)
monsters_router = router.register('monsters', MonsterViewSet)
melodies_router = router.register('melodies', MelodyViewSet)
owners_router = router.register('owners', OwnerViewSet)
