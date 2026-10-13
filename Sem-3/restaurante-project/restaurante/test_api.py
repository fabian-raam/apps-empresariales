from datetime import time
from decimal import Decimal

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Cliente, DetalleReserva, Mesa, Persona, Plato, Reserva
from .serializers import PlatoSerializer, ReservaReadSerializer


class RestauranteApiTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="API Entradas")
        self.plato = Plato.objects.create(
            categoria=self.categoria, nombre="Sopa API", precio="12.50", existencias=20
        )
        persona = Persona.objects.create(
            nombres="Ada", apellidos="Prueba", documento="API-001",
            telefono="900000001", correo="ada.api@example.test",
        )
        self.cliente = Cliente.objects.create(persona=persona)
        self.mesa = Mesa.objects.create(numero=801, capacidad=4)

    def crear_reserva(self, hora, estado="pendiente", nombre_plato=None):
        reserva = Reserva.objects.create(
            cliente=self.cliente, mesa=self.mesa, fecha=timezone.localdate(),
            hora=hora, cantidad_personas=2, estado=estado,
        )
        plato = self.plato
        if nombre_plato:
            plato = Plato.objects.create(
                categoria=self.categoria, nombre=nombre_plato,
                precio="8.00", existencias=10,
            )
        DetalleReserva.objects.create(
            reserva=reserva, plato=plato, cantidad=2,
            precio_unitario=plato.precio,
        )
        return reserva

    def test_plato_serializer_serializa_objeto_y_queryset(self):
        uno = PlatoSerializer(self.plato)
        varios = PlatoSerializer(Plato.objects.all(), many=True)
        self.assertEqual(uno.data["nombre"], "Sopa API")
        self.assertEqual(len(varios.data), 1)

    def test_plato_serializer_valida_precio_positivo(self):
        valido = PlatoSerializer(data={
            "categoria": self.categoria.pk, "nombre": "Arroz API",
            "precio": "10.00", "existencias": 5, "img_url": "",
        })
        self.assertTrue(valido.is_valid(), valido.errors)
        self.assertEqual(valido.validated_data["precio"], Decimal("10.00"))
        self.assertIsNotNone(valido.save())

        invalido = PlatoSerializer(data={
            "categoria": self.categoria.pk, "nombre": "Precio cero API",
            "precio": "0.00", "existencias": 5, "img_url": "",
        })
        self.assertFalse(invalido.is_valid())
        self.assertIn("precio", invalido.errors)

    def test_api_crud_codigos_http(self):
        lista = reverse("api-plato-list")
        self.assertEqual(self.client.get(lista).status_code, status.HTTP_200_OK)
        creado = self.client.post(lista, {
            "categoria": self.categoria.pk, "nombre": "Torta API",
            "precio": "18.00", "existencias": 7, "img_url": "",
        }, format="json")
        self.assertEqual(creado.status_code, status.HTTP_201_CREATED)
        plato_id = creado.data["plato_id"]
        detalle = reverse("api-plato-detail", args=[plato_id])
        self.assertEqual(self.client.get(detalle).status_code, status.HTTP_200_OK)

        invalido = self.client.post(lista, {
            "categoria": self.categoria.pk, "nombre": "Precio inválido",
            "precio": "0.00", "existencias": 3, "img_url": "",
        }, format="json")
        self.assertEqual(invalido.status_code, status.HTTP_400_BAD_REQUEST)

        actualizado = self.client.patch(detalle, {"precio": "20.00"}, format="json")
        self.assertEqual(actualizado.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(detalle).status_code, status.HTTP_204_NO_CONTENT)
        inexistente = reverse("api-plato-detail", args=[999999])
        self.assertEqual(self.client.get(inexistente).status_code, status.HTTP_404_NOT_FOUND)

    def test_search_ordering_y_router(self):
        Plato.objects.create(categoria=self.categoria, nombre="Torta", precio="22.00", existencias=3)
        self.assertEqual(self.client.get("/api/").status_code, status.HTTP_200_OK)
        encontrados = self.client.get(reverse("api-plato-list"), {"search": "sopa"})
        self.assertEqual([p["nombre"] for p in encontrados.data], ["Sopa API"])
        ordenados = self.client.get(reverse("api-plato-list"), {"ordering": "-precio"})
        self.assertEqual(ordenados.data[0]["nombre"], "Torta")
        combinados = self.client.get(reverse("api-plato-list"), {"search": "sopa", "ordering": "-precio"})
        self.assertEqual([p["nombre"] for p in combinados.data], ["Sopa API"])

    def test_reserva_anidada_filtro_y_accion_queryset(self):
        confirmada = self.crear_reserva(time(19, 0), "confirmada")
        self.crear_reserva(time(20, 0), "pendiente", "Postre API")
        detalle = reverse("api-reserva-detail", args=[confirmada.pk])
        respuesta = self.client.get(detalle)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data["cliente"]["persona"]["nombres"], "Ada")
        self.assertEqual(respuesta.data["detalles"][0]["plato"]["nombre"], "Sopa API")

        filtradas = self.client.get(reverse("api-reserva-list"), {"estado": "confirmada"})
        self.assertEqual(len(filtradas.data), 1)
        por_mes = self.client.get(reverse("api-reserva-mes-actual"))
        self.assertEqual(len(por_mes.data), 2)

    def test_queryset_anidado_reduce_consultas_de_serializacion(self):
        self.crear_reserva(time(19, 0), "confirmada")
        self.crear_reserva(time(20, 0), "pendiente", "Postre API")

        with CaptureQueriesContext(connection) as antes:
            ReservaReadSerializer(Reserva.objects.all(), many=True).data
        with CaptureQueriesContext(connection) as despues:
            queryset = (
                Reserva.objects.select_related("cliente__persona", "mesa", "ficha")
                .prefetch_related("solicitudes", "detalles__plato")
            )
            ReservaReadSerializer(queryset, many=True).data

        self.assertGreater(len(antes), len(despues))
