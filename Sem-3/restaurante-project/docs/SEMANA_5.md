# Semana 5: respuestas y capturas

Se utiliza el restaurante trabajado en Semanas 3 y 4 para ambas partes, siguiendo el desarrollo de la entrega anterior. Tiene diez entidades, por lo que se registran todas, no solamente las siete minimas. Si la investigacion entregada al docente pertenece a otro proyecto, la Parte 2 debe aplicarse tambien a ese proyecto.

No se agregaron modelos ni relaciones ni fue necesaria una nueva migracion. Las tres migraciones de restaurante estaban aplicadas al comenzar.

## Acceso local y evidencias

Servidor: http://127.0.0.1:8010/admin/

Cuenta local creada con el comando de Django `createsuperuser` en modo no interactivo: `semana5`. La clave aleatoria se encuentra en `.venv/semana5_acceso.json`. Este archivo, la base de datos y las herramientas de verificacion estan excluidos de Git. No incluir la clave en capturas ni en el Word.

Se prepararon datos identificados como DemoSemana5, mesa 505 y Sopa Semana 5. La reserva de ejemplo esta en http://127.0.0.1:8010/admin/restaurante/reserva/2/change/ . Tiene ficha, solicitud y detalle. Se conservaron los registros que existian antes.

Las capturas del navegador ya generadas estan en `.venv/capturas-semana5/`. Sus nombres indican los ejercicios donde sirven. Las capturas de codigo se toman en VS Code. No es necesario borrar o recrear migraciones para obtener evidencias.

Si el servidor esta detenido:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 8010
```

## Ejercicio 1

Texto: Se recupero la aplicacion del restaurante. La entidad principal es Reserva. Tiene una ficha mediante una relacion uno a uno, varias solicitudes mediante una relacion uno a muchos y varios platos mediante DetalleReserva, que guarda cantidad y precio. Las tres migraciones existentes estan aplicadas.

Capturas: en `restaurante/models.py`, mostrar Reserva.platos, FichaReserva.reserva, SolicitudReserva.reserva y DetalleReserva. En terminal ejecutar:

```powershell
.\.venv\Scripts\python.exe manage.py showmigrations restaurante
```

## Ejercicio 2

Texto: Se creo una cuenta de superusuario y se inicio sesion en el panel de administracion. Esta cuenta permite gestionar los datos del restaurante desde Django Admin.

Captura: panel http://127.0.0.1:8010/admin/ despues de iniciar sesion. Evidencia disponible: `02-03-09-panel-admin.png`.

Para repetir personalmente la creacion con otra cuenta, sin modificar la existente:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Ejercicio 3

Texto: Se registraron los diez modelos existentes mediante admin.site.register(). Todos aparecen en el panel y pueden administrarse desde sus respectivos formularios.

Capturas: las diez llamadas a `admin.site.register` al final de `restaurante/admin.py`, y la seccion Restaurante del panel. Los registros finales incluyen sus clases ModelAdmin porque el ejercicio 4 pide personalizarlos; no se mantienen registros simples duplicados.

## Ejercicio 4

Texto: Se personalizaron los listados de reservas y platos para mostrar sus datos principales. Tambien se incorporaron busquedas por datos del cliente y por nombre del plato.

Capturas de codigo: clases ReservaAdmin y PlatoAdmin en `restaurante/admin.py`, incluyendo list_display y search_fields.

Capturas del navegador: `/admin/restaurante/reserva/` y `/admin/restaurante/plato/`. En reservas buscar DemoSemana5. Evidencias disponibles: `04-05-10-busqueda-filtro.png` y `04-10-listado-platos.png`.

## Ejercicio 5

Texto: Se agregaron filtros por estado, fecha y mesa en el listado de reservas. Esto permite encontrar rapidamente las reservas que cumplen una condicion, como las confirmadas.

Capturas: list_filter de ReservaAdmin y el listado con el filtro Confirmada seleccionado. Abrir http://127.0.0.1:8010/admin/restaurante/reserva/?q=DemoSemana5&estado__exact=confirmada . Debe verse la barra de filtros y el resultado.

## Ejercicio 6

Texto: Se incorporo la ficha de la reserva dentro de su formulario usando StackedInline. Asi se puede editar la ocasion y las observaciones desde la misma pantalla. Cada reserva admite como maximo una ficha.

Capturas: FichaReservaInline y la propiedad inlines de ReservaAdmin. En el navegador abrir la reserva 2 y capturar el bloque Ficha de la reserva. Evidencia disponible: `06-07-08-11-12-13-creado.png`.

## Ejercicio 7

Texto: Se incorporo DetalleReserva mediante TabularInline. Desde una reserva se pueden agregar platos y editar la cantidad y el precio unitario en filas.

Capturas: DetalleReservaInline y el bloque Platos de la reserva en el formulario de la reserva 2. Deben verse plato, cantidad y precio unitario como columnas editables.

## Ejercicio 8

Texto: Desde el Admin se crearon, modificaron y eliminaron una ficha, una solicitud y un detalle de una reserva. Los cambios se guardaron al confirmar el formulario. El Admin facilita la gestion interna del restaurante, pero las paginas del menu y las funciones para los clientes siguen necesitando vistas y plantillas propias.

Capturas disponibles: `08-13-antes-crear.png`, `06-07-08-11-12-13-creado.png`, `08-13-editado.png`, `08-13-antes-eliminar.png` y `08-13-eliminado.png`. El borrado corresponde a los tres registros relacionados, conservando la reserva y el plato.

Recorrido: usuario autenticado -> /admin/ -> ReservaAdmin -> ORM -> SQLite -> plantilla del Admin -> respuesta en el navegador. Guardar registros nuevos corresponde a INSERT, editar a UPDATE, eliminar a DELETE y volver a abrir el formulario a SELECT.

## Ejercicio 9

Texto: Se registraron las diez entidades del restaurante: Persona, Cliente, Administrador, Mesa, Reserva, Categoria, Plato, FichaReserva, SolicitudReserva y DetalleReserva. Se conservaron las entidades de la entrega anterior y se incluyeron las nuevas relaciones de Semana 4.

Capturas: todas las llamadas a admin.site.register y el panel con los diez modelos. Reutilizar el panel del ejercicio 3 es valido porque se administra el mismo proyecto.

Checklist: hay diez ModelAdmin con list_display, busquedas configuradas y filtros adecuados. La ficha utiliza StackedInline y el detalle utiliza TabularInline. Se verifico el CRUD de las tres relaciones. El Admin cubre gestion interna; la experiencia del cliente sigue en las vistas y plantillas del restaurante.

## Ejercicio 10

Texto: Se personalizaron los modelos para mostrar sus datos mas importantes. Por ejemplo, Reserva muestra cliente, mesa, fecha y estado; Plato muestra nombre, categoria y precio; y Mesa muestra numero, capacidad y disponibilidad. Se agregaron busquedas y filtros para facilitar la consulta.

Capturas: ReservaAdmin, PlatoAdmin y MesaAdmin. En navegador capturar los listados de Reservas, Platos y Mesas. Para demostrar busqueda y filtro, buscar DemoSemana5 y seleccionar Confirmada en Reservas.

## Ejercicio 11

Texto: La ficha se administra dentro de la reserva mediante StackedInline. Esto permite modificar la informacion complementaria sin abrir otra pantalla.

Capturas: FichaReservaInline y el bloque Ficha de la reserva del formulario, igual que en el ejercicio 6.

## Ejercicio 12

Texto: Los platos de la reserva se administran mediante TabularInline. Cada fila permite elegir un plato y registrar su cantidad y precio acordado, que son datos propios de esa reserva.

Capturas: DetalleReservaInline y el bloque Platos de la reserva, igual que en el ejercicio 7.

## Ejercicio 13

Texto: Se verifico la creacion, edicion y eliminacion de datos relacionados usando los Inlines del Admin. Despues de guardar se volvio a consultar la informacion, comprobando que los cambios persistian. Se dejo una reserva de ejemplo con datos relacionados para repetir la demostracion.

Capturas: usar la secuencia del ejercicio 8. Para repetir manualmente sobre datos de ejemplo: cambiar la ocasion, marcar una solicitud como atendida y cambiar la cantidad y el precio; guardar y volver a abrir. Para eliminar una relacion, marcar su casilla Eliminar y guardar. No usar el boton rojo Eliminar de abajo, que elimina toda la reserva.

Para mostrar la persistencia en SQLite desde un proceso independiente, ejecutar tras guardar:

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "from restaurante.models import Reserva; r=Reserva.objects.get(pk=2); print(list(r.detalles.values('plato__nombre','cantidad','precio_unitario'))); print(list(r.solicitudes.values('descripcion','atendida'))); print(list(r._meta.apps.get_model('restaurante','FichaReserva').objects.filter(reserva=r).values('ocasion','observaciones')))"
```

La prueba `test_crud_de_las_tres_relaciones_por_inlines` tambien comprueba las altas, cambios y bajas sobre SQLite temporal, sin alterar los registros personales.

## Ejercicio 14

Texto: Se actualizaron README.md y requirements.txt para documentar los modelos registrados, las busquedas, los filtros y la edicion de relaciones dentro del Admin. Se publico el trabajo en el repositorio con el commit semana 5.

Repositorio: https://github.com/fabian-raam/apps-empresariales

Carpeta: Sem-3/restaurante-project.

Capturas: seccion Administracion de Semana 5 del README, requirements.txt y el commit semana 5 en GitHub. No incluir SQLite, claves locales ni el entorno virtual en la publicacion.

## Verificacion general

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
```

Resultado de la verificacion: 21 pruebas correctas, sin errores de configuracion ni cambios de modelos pendientes. Se verifico tambien el CRUD real del Admin en Chrome, la busqueda, los filtros y la persistencia de los datos de ejemplo en SQLite.

## Conclusiones

1. Se centralizo la gestion de los datos del restaurante en el panel de administracion.
2. Se facilitaron las consultas con busquedas y filtros, y la edicion de datos relacionados desde una sola pantalla.
3. Se comprobaron los cambios y se documento el proyecto para facilitar su revision y mantenimiento.
