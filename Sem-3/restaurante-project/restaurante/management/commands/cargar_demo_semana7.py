from datetime import date, time

from django.core.management.base import BaseCommand

from restaurante.models import (
    Categoria, Cliente, DetalleReserva, FichaReserva, Mesa, Persona, Plato,
    Reserva, SolicitudReserva,
)


class Command(BaseCommand):
    help = "Crea datos de demostración idempotentes para los ejercicios de la Semana 7."

    def handle(self, *args, **options):
        categoria, _ = Categoria.objects.get_or_create(
            nombre="Demo Semana 7", defaults={"activa": True}
        )
        platos = []
        for nombre, precio in (("Sopa Demo S7", "12.50"), ("Arroz Demo S7", "18.00"), ("Postre Demo S7", "8.00")):
            plato, _ = Plato.objects.get_or_create(
                nombre=nombre,
                defaults={"categoria": categoria, "precio": precio, "existencias": 100},
            )
            platos.append(plato)

        reservas = []
        for i in range(1, 6):
            persona, _ = Persona.objects.get_or_create(
                documento=f"S7DEMO{i:04d}",
                defaults={
                    "nombres": f"Cliente Demo {i}", "apellidos": "Semana Siete",
                    "telefono": f"90000000{i}", "correo": f"s7demo{i}@example.test",
                },
            )
            cliente, _ = Cliente.objects.get_or_create(persona=persona)
            mesa, _ = Mesa.objects.get_or_create(
                numero=9700 + i,
                defaults={"capacidad": 6, "disponible": True},
            )
            reserva, _ = Reserva.objects.get_or_create(
                cliente=cliente, mesa=mesa,
                fecha=date(2026, 9, 20 + i), hora=time(18 + i, 0),
                defaults={"cantidad_personas": i % 4 + 1, "estado": ("pendiente", "confirmada", "cancelada", "confirmada", "pendiente")[i - 1]},
            )
            reservas.append(reserva)
            FichaReserva.objects.get_or_create(
                reserva=reserva,
                defaults={"ocasion": "Demostración Semana 7", "observaciones": "Dato ficticio para la práctica."},
            )

        pares = ((0, 0, 2), (0, 1, 1), (1, 0, 1), (1, 2, 2),
                 (2, 1, 3), (2, 2, 1), (3, 0, 2), (4, 2, 2))
        for reserva_i, plato_i, cantidad in pares:
            DetalleReserva.objects.get_or_create(
                reserva=reservas[reserva_i], plato=platos[plato_i],
                defaults={"cantidad": cantidad, "precio_unitario": platos[plato_i].precio},
            )
        for i, reserva in enumerate(reservas[:3], start=1):
            SolicitudReserva.objects.get_or_create(
                reserva=reserva, descripcion=f"Solicitud demo Semana 7 #{i}",
                defaults={"atendida": i == 2},
            )

        self.stdout.write(self.style.SUCCESS(
            "Datos de Semana 7 listos: 5 reservas, 3 solicitudes y 8 detalles demo."
        ))
