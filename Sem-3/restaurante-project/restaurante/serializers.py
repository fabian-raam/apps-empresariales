from rest_framework import serializers

from .models import (
    Categoria,
    Cliente,
    DetalleReserva,
    FichaReserva,
    Mesa,
    Persona,
    Plato,
    Reserva,
    SolicitudReserva,
)


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = ("plato_id", "categoria", "nombre", "precio", "existencias", "img_url")

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return value


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ("categoria_id", "nombre", "activa")


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ("mesa_id", "numero", "capacidad", "disponible")

    def validate_capacidad(self, value):
        if value < 1:
            raise serializers.ValidationError("La capacidad debe ser al menos uno.")
        return value


class PersonaResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ("nombres", "apellidos")


class ClienteResumenSerializer(serializers.ModelSerializer):
    persona = PersonaResumenSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = ("cliente_id", "persona")


class PlatoResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = ("plato_id", "nombre", "precio")


class FichaReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaReserva
        fields = ("ocasion", "observaciones")


class SolicitudReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudReserva
        fields = ("descripcion", "atendida")


class DetalleReservaReadSerializer(serializers.ModelSerializer):
    plato = PlatoResumenSerializer(read_only=True)

    class Meta:
        model = DetalleReserva
        fields = ("detalle_id", "plato", "cantidad", "precio_unitario")


class ReservaReadSerializer(serializers.ModelSerializer):
    cliente = ClienteResumenSerializer(read_only=True)
    ficha = FichaReservaSerializer(read_only=True, allow_null=True)
    solicitudes = SolicitudReservaSerializer(many=True, read_only=True)
    detalles = DetalleReservaReadSerializer(many=True, read_only=True)

    class Meta:
        model = Reserva
        fields = (
            "reserva_id", "cliente", "mesa", "fecha", "hora",
            "cantidad_personas", "estado", "ficha", "solicitudes", "detalles",
        )
