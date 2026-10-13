from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Categoria, Mesa, Plato, Reserva
from .serializers import (
    CategoriaSerializer,
    MesaSerializer,
    PlatoSerializer,
    ReservaReadSerializer,
)


class PlatoViewSet(viewsets.ModelViewSet):
    queryset = Plato.objects.select_related("categoria").all()
    serializer_class = PlatoSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("nombre", "categoria__nombre")
    ordering_fields = ("nombre", "precio", "existencias")
    ordering = ("nombre",)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (AllowAny,)


class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = (AllowAny,)


class ReservaReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservaReadSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = (
            Reserva.objects.select_related("cliente__persona", "mesa", "ficha")
            .prefetch_related("solicitudes", "detalles__plato")
            .all()
        )
        queryset = queryset.con_estado(self.request.query_params.get("estado"))
        return queryset.del_mes_actual(self.request.query_params.get("mes") == "actual")

    @action(detail=False, methods=("get",), url_path="mes-actual")
    def mes_actual(self, request):
        reservas = self.get_queryset().del_mes_actual(True)
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data)
