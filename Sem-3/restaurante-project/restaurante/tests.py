from django.db import IntegrityError
from django.test import TransactionTestCase, Client as HttpClient
from django.urls import reverse
from .models import Persona, Cliente, Administrador, Mesa, Reserva, Categoria, Plato


class RestauranteTests(TransactionTestCase):
    def setUp(self):
        self.persona = Persona.objects.create(nombres="Ana", apellidos="Pérez", documento="123", telefono="999999999", correo="ana@example.com")
        self.cliente = Cliente.objects.create(persona=self.persona)
        self.mesa = Mesa.objects.create(numero=1, capacidad=4)
        self.categoria = Categoria.objects.create(nombre="Entradas")

    def url(self, tipo, accion, pk=None):
        return reverse(f"restaurante:{tipo}_{accion}", args=[pk] if pk else [])

    def personales(self, **extra):
        return dict(nombres="Luis", apellidos="Torres", documento="456", telefono="987654321", correo="luis@example.com", **extra)

    def reserva_datos(self, **extra):
        datos = dict(cliente=self.cliente.pk, mesa=self.mesa.pk, fecha="2026-10-10", hora="19:00", cantidad_personas=2, estado="pendiente")
        datos.update(extra)
        return datos

    def test_registro_cliente_crea_persona_y_cliente(self):
        response = self.client.post(self.url("cliente", "crear"), self.personales())
        self.assertRedirects(response, self.url("cliente", "lista"))
        self.assertEqual(Persona.objects.count(), 2)
        self.assertEqual(Cliente.objects.get(persona__documento="456").persona.correo, "luis@example.com")
        self.assertNotContains(self.client.get(self.url("cliente", "crear")), 'name="persona"')

    def test_registro_administrador_y_edicion_persona(self):
        self.client.post(self.url("administrador", "crear"), self.personales(fecha_contratacion="2026-09-01"))
        administrador = Administrador.objects.get()
        datos = self.personales(fecha_contratacion="2026-09-02")
        datos["nombres"] = "Lucía"
        response = self.client.post(self.url("administrador", "editar", administrador.pk), datos)
        self.assertRedirects(response, self.url("administrador", "lista"))
        administrador.refresh_from_db()
        self.assertEqual(administrador.persona.nombres, "Lucía")
        self.assertEqual(Persona.objects.count(), 2)
        self.assertContains(self.client.get(self.url("administrador", "editar", administrador.pk)), "2026-09-02")

    def test_administrador_invalido_no_guarda_persona(self):
        response = self.client.post(
            self.url("administrador", "crear"),
            self.personales(fecha_contratacion="fecha incorrecta"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Persona.objects.count(), 1)
        self.assertEqual(Administrador.objects.count(), 0)

    def test_persona_duplicada_no_crea_rol(self):
        datos = self.personales()
        datos["documento"] = self.persona.documento
        response = self.client.post(self.url("cliente", "crear"), datos)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(Persona.objects.count(), 1)

    def test_crud_todos_los_modelos(self):
        casos = [
            ("cliente", Cliente, self.personales(), "nombres", "Nuevo"),
            ("administrador", Administrador, self.personales(fecha_contratacion="2026-09-01"), "nombres", "Nuevo"),
            ("mesa", Mesa, dict(numero=2, capacidad=6, disponible="on"), "capacidad", 8),
            ("categoria", Categoria, dict(nombre="Fondos", activa="on"), "nombre", "Postres"),
            ("plato", Plato, dict(nombre="Sopa", precio="12.50", categoria=self.categoria.pk, img_url=""), "nombre", "Ensalada"),
            ("reserva", Reserva, self.reserva_datos(), "estado", "confirmada"),
        ]
        for tipo, modelo, datos, campo, valor in casos:
            with self.subTest(tipo=tipo):
                self.assertEqual(self.client.get(self.url(tipo, "crear")).status_code, 200)
                response = self.client.post(self.url(tipo, "crear"), datos)
                self.assertRedirects(response, self.url(tipo, "lista"))
                objeto = modelo.objects.latest(modelo._meta.pk.name)
                self.assertContains(self.client.get(self.url(tipo, "lista")), self.url(tipo, "editar", objeto.pk))
                self.assertEqual(self.client.get(self.url(tipo, "editar", objeto.pk)).status_code, 200)
                datos[campo] = valor
                self.assertRedirects(self.client.post(self.url(tipo, "editar", objeto.pk), datos), self.url(tipo, "lista"))
                objeto.refresh_from_db()
                self.assertEqual(getattr(objeto.persona if tipo in ("cliente", "administrador") else objeto, campo), valor)
                self.assertEqual(self.client.get(self.url(tipo, "eliminar", objeto.pk)).status_code, 200)
                self.assertTrue(modelo.objects.filter(pk=objeto.pk).exists())
                self.assertEqual(self.client.delete(self.url(tipo, "eliminar", objeto.pk)).status_code, 200)
                self.assertTrue(modelo.objects.filter(pk=objeto.pk).exists())
                self.assertRedirects(self.client.post(self.url(tipo, "eliminar", objeto.pk)), self.url(tipo, "lista"))
                self.assertFalse(modelo.objects.filter(pk=objeto.pk).exists())
                if tipo in ("cliente", "administrador"):
                    self.assertTrue(Persona.objects.filter(pk=objeto.persona_id).exists())
                    Persona.objects.filter(pk=objeto.persona_id).delete()

    def test_reserva_duplicada_y_restriccion_bd(self):
        datos = self.reserva_datos()
        self.client.post(self.url("reserva", "crear"), datos)
        response = self.client.post(self.url("reserva", "crear"), datos)
        self.assertContains(response, "ya tiene una reserva")
        self.assertEqual(Reserva.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.cliente, mesa=self.mesa, fecha="2026-10-10", hora="19:00", cantidad_personas=2)
        reserva = Reserva.objects.get()
        self.assertRedirects(self.client.post(self.url("reserva", "editar", reserva.pk), datos), self.url("reserva", "lista"))

    def test_validaciones_reserva(self):
        for cambios in [dict(cantidad_personas=0), dict(cantidad_personas=-1), dict(cantidad_personas=5), dict(estado="invalido")]:
            with self.subTest(cambios=cambios):
                response = self.client.post(self.url("reserva", "crear"), self.reserva_datos(**cambios))
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
        self.assertEqual(Reserva.objects.count(), 0)
        otra = Mesa.objects.create(numero=2, capacidad=4, disponible=False)
        response = self.client.get(self.url("reserva", "crear"))
        self.assertNotIn(otra, response.context["form"].fields["mesa"].queryset)
        self.client.post(self.url("reserva", "crear"), self.reserva_datos(mesa=otra.pk))
        self.assertEqual(Reserva.objects.count(), 0)

    def test_cancelar_conserva_y_no_libera_horario(self):
        self.client.post(self.url("reserva", "crear"), self.reserva_datos())
        reserva = Reserva.objects.get()
        url = self.url("reserva", "cancelar", reserva.pk)
        self.assertEqual(self.client.get(url).status_code, 200)
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, "pendiente")
        self.assertEqual(self.client.delete(url).status_code, 200)
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, "pendiente")
        self.assertRedirects(self.client.post(url), self.url("reserva", "lista"))
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, "cancelada")
        self.assertContains(self.client.post(self.url("reserva", "crear"), self.reserva_datos()), "ya tiene una reserva")

    def test_editar_reserva_mesa_actual_no_disponible(self):
        self.client.post(self.url("reserva", "crear"), self.reserva_datos())
        reserva = Reserva.objects.get()
        self.mesa.disponible = False
        self.mesa.save()
        self.assertRedirects(self.client.post(self.url("reserva", "editar", reserva.pk), self.reserva_datos(estado="confirmada")), self.url("reserva", "lista"))

    def test_no_reducir_capacidad_con_reservas(self):
        self.client.post(self.url("reserva", "crear"), self.reserva_datos())
        response = self.client.post(self.url("mesa", "editar", self.mesa.pk), dict(numero=1, capacidad=1, disponible="on"))
        self.assertContains(response, "Existen reservas")
        self.mesa.refresh_from_db()
        self.assertEqual(self.mesa.capacidad, 4)

    def test_eliminar_cliente_muestra_cascada(self):
        self.client.post(self.url("reserva", "crear"), self.reserva_datos())
        response = self.client.get(self.url("cliente", "eliminar", self.cliente.pk))
        self.assertContains(response, "También se eliminarán")
        self.assertContains(response, "Reserva de")
        self.client.post(self.url("cliente", "eliminar", self.cliente.pk))
        self.assertFalse(Cliente.objects.exists())
        self.assertFalse(Reserva.objects.exists())
        self.assertTrue(Mesa.objects.exists())

    def test_menu_filtro_y_paginas(self):
        otra = Categoria.objects.create(nombre="Postres", activa=False)
        Plato.objects.create(nombre="Sopa", precio=10, categoria=self.categoria)
        Plato.objects.create(nombre="Torta", precio=8, categoria=otra)
        self.assertEqual(self.client.get(reverse("restaurante:inicio")).status_code, 200)
        menu = reverse("restaurante:menu")
        self.assertContains(self.client.get(menu), "Torta")
        response = self.client.get(menu, {"categoria": self.categoria.pk})
        self.assertContains(response, "Sopa")
        self.assertNotContains(response, "Torta")
        self.assertEqual(self.client.get(menu, {"categoria": "invalida"}).status_code, 200)
        self.assertEqual(self.client.get(self.url("mesa", "editar", 99999)).status_code, 404)

    def test_csrf_obligatorio(self):
        navegador = HttpClient(enforce_csrf_checks=True)
        self.assertEqual(navegador.post(self.url("mesa", "eliminar", self.mesa.pk)).status_code, 403)
        self.assertContains(navegador.get(self.url("mesa", "crear")), "csrfmiddlewaretoken")

    def test_no_hay_registro_independiente_de_personas(self):
        self.assertNotContains(self.client.get(reverse("restaurante:inicio")), "/personas/")
        for ruta in ["/personas/", "/personas/crear/", "/personas/1/editar/", "/personas/1/eliminar/"]:
            self.assertEqual(self.client.get(ruta).status_code, 404)
            self.assertEqual(self.client.post(ruta, self.personales()).status_code, 404)
        self.assertEqual(Persona.objects.count(), 1)
        for tipo in ["cliente", "administrador"]:
            response = self.client.get(self.url(tipo, "crear"))
            for campo in ["nombres", "apellidos", "documento", "telefono", "correo"]:
                self.assertContains(response, f'name="{campo}"')
            self.assertNotContains(response, 'name="persona"')
