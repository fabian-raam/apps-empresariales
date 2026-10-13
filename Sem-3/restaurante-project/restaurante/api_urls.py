from rest_framework.routers import DefaultRouter

from .api_views import CategoriaViewSet, MesaViewSet, PlatoViewSet, ReservaReadOnlyViewSet

router = DefaultRouter()
router.register("platos", PlatoViewSet, basename="api-plato")
router.register("categorias", CategoriaViewSet, basename="api-categoria")
router.register("mesas", MesaViewSet, basename="api-mesa")
router.register("reservas", ReservaReadOnlyViewSet, basename="api-reserva")

urlpatterns = router.urls
