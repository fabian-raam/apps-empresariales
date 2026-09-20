from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import (
    Persona, Cliente, Administrador, Categoria, Plato, Mesa, Reserva,
    FichaReserva, SolicitudReserva, DetalleReserva,
)


class RestauranteAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_superuser(
            username="prueba_admin", password="Solo-para-pruebas-2026"
        )
        persona = Persona.objects.create(
            nombres="PruebaAdmin", apellidos="Restaurante", documento="ADMIN01",
            telefono="999111222", correo="admin-test@example.com",
        )
        cls.cliente = Cliente.objects.create(persona=persona)
        cls.mesa = Mesa.objects.create(numero=50, capacidad=4)
        categoria = Categoria.objects.create(nombre="Entradas de prueba")
        cls.plato = Plato.objects.create(nombre="Sopa de prueba", precio=12, categoria=categoria)

    def setUp(self):
        self.client.force_login(self.usuario)

    def datos(self):
        return {
            "cliente": self.cliente.pk, "mesa": self.mesa.pk,
            "fecha": "2026-10-20", "hora": "19:00:00",
            "cantidad_personas": 2, "estado": "pendiente", "_save": "Guardar",
            "ficha-TOTAL_FORMS": 1, "ficha-INITIAL_FORMS": 0,
            "ficha-MIN_NUM_FORMS": 0, "ficha-MAX_NUM_FORMS": 1,
            "ficha-0-ocasion": "Aniversario", "ficha-0-observaciones": "Mesa tranquila",
            "solicitudes-TOTAL_FORMS": 1, "solicitudes-INITIAL_FORMS": 0,
            "solicitudes-MIN_NUM_FORMS": 0, "solicitudes-MAX_NUM_FORMS": 1000,
            "solicitudes-0-descripcion": "Silla infantil",
            "detalles-TOTAL_FORMS": 1, "detalles-INITIAL_FORMS": 0,
            "detalles-MIN_NUM_FORMS": 0, "detalles-MAX_NUM_FORMS": 1000,
            "detalles-0-plato": self.plato.pk, "detalles-0-cantidad": 2,
            "detalles-0-precio_unitario": "12.00",
        }

    def test_modelos_registrados_y_listados(self):
        for modelo in (Persona, Cliente, Administrador, Categoria, Plato, Mesa,
                       Reserva, FichaReserva, SolicitudReserva, DetalleReserva):
            with self.subTest(modelo=modelo.__name__):
                self.assertTrue(admin.site.is_registered(modelo))
                self.assertEqual(self.client.get(reverse(
                    f"admin:restaurante_{modelo._meta.model_name}_changelist"
                )).status_code, 200)

    def test_crud_de_las_tres_relaciones_por_inlines(self):
        datos = self.datos()
        crear = reverse("admin:restaurante_reserva_add")
        self.assertContains(self.client.get(crear), 'name="ficha-0-ocasion"')
        response = self.client.post(crear, datos)
        self.assertEqual(response.status_code, 302)
        reserva = Reserva.objects.get()
        ficha = FichaReserva.objects.get(reserva=reserva)
        solicitud = SolicitudReserva.objects.get(reserva=reserva)
        detalle = DetalleReserva.objects.get(reserva=reserva)
        self.assertEqual(detalle.cantidad, 2)
        self.assertEqual(ficha.ocasion, "Aniversario")

        editar = reverse("admin:restaurante_reserva_change", args=[reserva.pk])
        self.assertContains(self.client.get(editar), "Silla infantil")
        for prefijo, objeto in (("ficha", ficha), ("solicitudes", solicitud), ("detalles", detalle)):
            datos[f"{prefijo}-INITIAL_FORMS"] = 1
            datos[f"{prefijo}-0-{objeto._meta.pk.name}"] = objeto.pk
            datos[f"{prefijo}-0-reserva"] = reserva.pk
        datos.update({"ficha-0-ocasion": "Cumpleanos", "solicitudes-0-atendida": "on",
                      "detalles-0-cantidad": 3, "detalles-0-precio_unitario": "11.00"})
        self.assertEqual(self.client.post(editar, datos).status_code, 302)
        ficha.refresh_from_db()
        solicitud.refresh_from_db()
        detalle.refresh_from_db()
        self.assertEqual(ficha.ocasion, "Cumpleanos")
        self.assertTrue(solicitud.atendida)
        self.assertEqual(detalle.cantidad, 3)
        self.assertEqual(str(detalle.precio_unitario), "11.00")

        for prefijo in ("ficha", "solicitudes", "detalles"):
            datos[f"{prefijo}-0-DELETE"] = "on"
        self.assertEqual(self.client.post(editar, datos).status_code, 302)
        self.assertFalse(FichaReserva.objects.exists())
        self.assertFalse(SolicitudReserva.objects.exists())
        self.assertFalse(DetalleReserva.objects.exists())
        self.assertTrue(Reserva.objects.filter(pk=reserva.pk).exists())
        self.assertTrue(Plato.objects.filter(pk=self.plato.pk).exists())

    def test_inline_invalido_no_guarda_reserva_ni_relaciones(self):
        for cambios in ({"detalles-0-cantidad": 0}, {"detalles-0-precio_unitario": "-1"}):
            response = self.client.post(reverse("admin:restaurante_reserva_add"), {**self.datos(), **cambios})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(any(f.formset.errors for f in response.context["inline_admin_formsets"]))
            self.assertFalse(Reserva.objects.exists())
            self.assertFalse(FichaReserva.objects.exists())

    def test_busqueda_y_filtro(self):
        self.client.post(reverse("admin:restaurante_reserva_add"), self.datos())
        listado = reverse("admin:restaurante_reserva_changelist")
        self.assertEqual(self.client.get(listado, {"q": "PruebaAdmin"}).context["cl"].result_count, 1)
        self.assertEqual(self.client.get(listado, {"q": "NoExiste"}).context["cl"].result_count, 0)
        self.assertEqual(self.client.get(listado, {"estado__exact": "pendiente"}).context["cl"].result_count, 1)
        self.assertEqual(self.client.get(listado, {"estado__exact": "cancelada"}).context["cl"].result_count, 0)

    def test_acceso_requiere_staff_y_permisos(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)
        usuario = get_user_model().objects.create_user(username="sin_permisos", is_staff=True)
        self.client.force_login(usuario)
        self.assertEqual(self.client.get(reverse("admin:restaurante_reserva_add")).status_code, 403)
