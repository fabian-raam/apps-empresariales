# Semana 7: ORM avanzado del restaurante

Se aplica la práctica a la aplicación disponible en este repositorio. No se crean entidades nuevas: `Plato.existencias` agrega el entero necesario para el descuento de inventario. `Reserva` es la entidad principal; sus relaciones son `FichaReserva` (1:1), `SolicitudReserva` (1:N) y `Plato` (N:M mediante `DetalleReserva`). El estado es `Reserva.estado` y los atributos numéricos del modelo intermedio son `cantidad` y `precio_unitario`.

El documento de laboratorio pide una segunda parte sobre la investigación propia. Este repositorio contiene una sola aplicación de restaurante, así que se reutiliza esta misma aplicación para ambas partes. Si la investigación individual del estudiante está en otro proyecto, la Parte 2 deberá trasladarse también a ese proyecto.

## Cambios implementados

- `Plato.existencias`, con migración `0004_plato_existencias.py` y valor inicial 100 para platos existentes.
- `/reservas/operacion/`: formulario de operación. En una transacción, descuenta existencias mediante `F()`, crea una reserva y crea el detalle con el precio actual. Una insuficiencia de stock o error de validación revierte todos los cambios. Al completarse redirige al listado (Post/Redirect/Get).
- `/reportes/`: total global y unidades mediante `aggregate()`, total y número de detalles por reserva mediante `annotate()`, y resumen de reservas/unidades agrupado por estado con `values().annotate()`.
- `ReservaQuerySet`, conectado con `as_manager()`: `con_estado()` y `del_mes_actual()` son encadenables y se usan en `reserva_lista` y `reporte`.
- `reserva_lista` y `plato_lista` precargan relaciones con `select_related()` y `prefetch_related()`.
- `python manage.py cargar_demo_semana7`: comando repetible que crea cinco reservas demo, tres solicitudes y ocho detalles ligados a tres platos. Ya se ejecutó en la base local. Los nombres y datos son ficticios.

## Respuestas y capturas por ejercicio

### Parte 1

1. **Campos y relaciones:** la entidad principal es `Reserva`; ficha 1:1, solicitudes 1:N y platos N:M mediante `DetalleReserva`. Se añade `Plato.existencias` para descontar unidades; `Reserva.estado` sirve como estado y `DetalleReserva.cantidad`/`precio_unitario` como datos del intermedio. Mostrar los modelos y la migración `0004`.
2. **Datos de prueba:** ejecutar `python manage.py cargar_demo_semana7`. Verificar cinco reservas, tres solicitudes y ocho detalles con los nombres “Demo Semana 7”. Capturar listados en Django Admin.
3. **Transacción:** abrir `/reservas/operacion/`, registrar una reserva con cantidad válida y comprobar el detalle y el stock reducido. Repetir con cantidad superior a las existencias: se muestra error y no debe quedar reserva, detalle ni descuento. El bloque `transaction.atomic()` y el `update(existencias=F("existencias") - cantidad)` están en `reserva_operacion`.
4. **aggregate:** en `python manage.py shell`:

   ```python
   from django.db.models import DecimalField, F, Sum
   from restaurante.models import DetalleReserva
   DetalleReserva.objects.aggregate(monto=Sum(F("cantidad") * F("precio_unitario"), output_field=DecimalField(max_digits=14, decimal_places=2)))
   ```

   Devuelve un diccionario porque calcula un resultado global, no una fila de objetos.
5. **annotate y agrupación:** `reporte` agrega número de detalles y total a cada reserva, y agrupa por estado para contar reservas y sumar unidades. Mostrar la salida del reporte o consultar en shell:

   ```python
   from django.db.models import Count, F, Sum
   from restaurante.models import Reserva
   list(Reserva.objects.annotate(detalles=Count("detalles", distinct=True)).values("reserva_id", "detalles"))
   list(Reserva.objects.values("estado").annotate(reservas=Count("pk", distinct=True), unidades=Sum("detalles__cantidad")).order_by("-reservas"))
   ```
6. **Página de reporte:** `/reportes/` hereda de `base.html`, presenta las tres consultas y aplica `floatformat:2` al importe.
7. **QuerySet personalizado:** `ReservaQuerySet` aporta `con_estado()` y `del_mes_actual()`, y `Reserva.objects` lo expone mediante `as_manager()`. Los dos métodos se aplican desde los listados y reportes; el filtro solo restringe datos cuando se solicita por parámetros, por lo que el CRUD completo permanece disponible.
8. **N+1 y optimización:** la vista de platos ya carga la categoría y detalles/reservas anticipadamente. En shell, medir una consulta equivalente sin optimizar y otra con la estrategia de la vista:

   ```python
   from django.db import connection, reset_queries
   from restaurante.models import Plato
   reset_queries()
   for plato in Plato.objects.all():
       for detalle in plato.detalles_reserva.all():
           _ = detalle.reserva.fecha
   print("Antes:", len(connection.queries))
   reset_queries()
   for plato in Plato.objects.select_related("categoria").prefetch_related("detalles_reserva__reserva"):
       for detalle in plato.detalles_reserva.all():
           _ = (plato.categoria.nombre, detalle.reserva.fecha)
   print("Después:", len(connection.queries))
   ```

   `select_related()` une relaciones de un solo objeto (ForeignKey/OneToOne); `prefetch_related()` hace consultas adicionales agrupadas para relaciones múltiples.

   En la base local preparada para las capturas, la medición dio **14 consultas antes y 3 después**. El conteo inicial puede variar si agregas o eliminas datos; vuelve a ejecutar ambos bloques en el mismo estado de la base para comparar.

### Parte 2: aplicación de investigación

En este repositorio corresponde al mismo sistema de restaurante descrito arriba; la implementación es compartida, no duplicada. Si se evalúa la Parte 2 como una investigación distinta, aplicar las mismas técnicas a sus propios modelos.

9. **Equivalencias:** entero `Plato.existencias`; estado `Reserva.estado`; intermedio `DetalleReserva.cantidad` y `precio_unitario`; operación: crear Reserva + DetalleReserva y descontar Plato.
10. **Transacción:** `/reservas/operacion/`, con caso exitoso y caso de rollback por existencias insuficientes.
11. **Reportes:** `/reportes/`, con agregado monetario y resumen anotado/agrupado.
12. **QuerySet:** `ReservaQuerySet` y sus dos filtros encadenables, usados por vistas existentes.
13. **Optimización:** listado `/platos/`; contar consultas con el snippet del ejercicio 8 antes/después.
14. **Publicación:** README y requirements describen los cambios; `requirements.txt` no requiere paquetes nuevos. El commit y push deben hacerse desde una sesión GitHub autenticada.

## Rutas

- Operación transaccional: `/reservas/operacion/`
- Reporte: `/reportes/`
- Filtros opcionales del listado: `/reservas/?estado=confirmada&mes=actual`
- Carga repetible de datos de práctica: `python manage.py cargar_demo_semana7`

No incluir claves ni datos personales reales en las capturas.
