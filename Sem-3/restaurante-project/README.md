# Sistema de reservas de restaurante

Proyecto Django de reservas de restaurante, ampliado en la Semana 4 con relaciones uno a uno, uno a muchos y muchos a muchos mediante un modelo intermedio con CRUD propio.

Repositorio: https://github.com/fabian-raam/apps-empresariales

Carpeta del proyecto: `Sem-3/restaurante-project`.

## Integrantes y división del trabajo

Los diez requisitos originales de la Semana 3 se distribuyeron en cinco para cada integrante. La tabla conserva ese reparto previo.

| Integrante | Requisito | Funciones en `restaurante/views.py` |
| --- | --- | --- |
| Oscar Eneque | 1. Registrar clientes con nombre, teléfono y correo electrónico. | `cliente_crear` |
| Oscar Eneque | 2. Listar y actualizar los clientes registrados. | `cliente_lista`, `cliente_editar` |
| Oscar Eneque | 3. Registrar mesas con número, capacidad y disponibilidad. | `mesa_crear` |
| Oscar Eneque | 4. Listar, actualizar y eliminar mesas. | `mesa_lista`, `mesa_editar`, `mesa_eliminar` |
| Oscar Eneque | 6. Listar reservas mostrando cliente, mesa, fecha, hora y cantidad de personas. | `reserva_lista` |
| Fabian Ramirez | 5. Registrar reservas asociadas con un cliente y una mesa. | `reserva_crear` |
| Fabian Ramirez | 7. Actualizar y cancelar reservas. | `reserva_editar`, `reserva_cancelar` |
| Fabian Ramirez | 8. Registrar, listar, actualizar y eliminar categorías del menú. | `categoria_crear`, `categoria_lista`, `categoria_editar`, `categoria_eliminar` |
| Fabian Ramirez | 9. Registrar platos con categoría, nombre y precio. | `plato_crear` |
| Fabian Ramirez | 10. Listar, actualizar y eliminar platos. | `plato_lista`, `plato_editar`, `plato_eliminar` |

Cada integrante se encarga también de los formularios, rutas, plantillas y pruebas correspondientes a sus requisitos. La configuración del proyecto, los modelos compartidos, el README y las dependencias se revisan entre ambos.

## Problemática y usuarios

El registro manual de mesas, clientes y horarios puede causar reservas duplicadas y errores de capacidad. Este sistema centraliza las reservas y permite consultar el menú por categoría.

- Clientes: personas que reservan mesas y consultan el menú.
- Administradores y personal del restaurante: gestionan clientes, mesas, reservas y platos.
- Superusuarios de Django: gestionan los siete modelos originales registrados en `/admin/`.

Las pantallas del ejercicio son de acceso público y no implementan autenticación por roles. El modelo Administrador representa datos del personal; registrarlo no crea una cuenta de Django ni concede acceso al Admin.

## Requisitos funcionales

- Navegación a las secciones originales, al menú y a los detalles de reserva.
- Crear, listar, editar y eliminar detalles de reserva, seleccionando reserva y plato e indicando cantidad y precio unitario.
- Mostrar la ficha y las solicitudes de cada reserva, y los pedidos asociados a cada plato. Fichas y solicitudes no tienen formulario web propio; pueden registrarse mediante ORM.
- Crear, listar, editar y eliminar clientes, administradores, mesas, reservas, categorías y platos. Persona se guarda internamente desde los formularios de cliente y administrador; no tiene una sección independiente en la web.
- Registrar y editar Persona junto con Cliente o Administrador con guardados consecutivos. No se selecciona una Persona preexistente en esos formularios.
- Validar documento y correo únicos, estados de reserva, cantidad positiva y capacidad de mesa.
- Ofrecer solo mesas disponibles al crear reservas. Al editar, también se admite la mesa actual para poder gestionar una reserva cuya mesa haya dejado de estar disponible.
- Impedir reservas duplicadas por mesa, fecha y hora tanto en formularios como mediante restricción de base de datos.
- Cancelar reservas conservando su registro. Se respeta la restricción original: una reserva cancelada también ocupa su combinación mesa/fecha/hora. Para reutilizarla, editar el registro existente o eliminarlo explícitamente.
- Confirmar eliminaciones; únicamente POST modifica o elimina datos y todos los formularios POST incluyen CSRF. Las confirmaciones originales muestran reservas o platos relacionados, pero no enumeran todos los nuevos registros dependientes.
- Consultar todos los platos agrupados o filtrados por categoría. Los platos siempre están disponibles, incluso si su categoría está marcada como inactiva; `img_url` es opcional.
- Interfaz reutilizable en español, con CSS adaptable a dispositivos móviles.

## Entidades y relaciones

| Entidad | Relaciones |
| --- | --- |
| Persona | Datos personales; documento y correo únicos |
| Cliente | OneToOne con Persona |
| Administrador | OneToOne con Persona y fecha de contratación |
| Mesa | Número único, capacidad y disponibilidad |
| Reserva | ForeignKey con Cliente y Mesa; fecha, hora, cantidad y estado |
| Categoria | Nombre único y estado activa |
| Plato | ForeignKey con Categoria; nombre, precio e imagen opcional |
| FichaReserva | OneToOne con Reserva; ocasión y observaciones opcionales |
| SolicitudReserva | ForeignKey con Reserva; descripción y estado de atención |
| DetalleReserva | ForeignKey con Reserva y Plato; cantidad y precio unitario acordado |

El modelo ampliado tiene diez entidades. `Reserva.platos` utiliza `ManyToManyField(through="DetalleReserva", related_name="reservas")`.

La relación 1:1 permite que una reserva tenga como máximo una ficha opcional, separando la información complementaria del registro principal. Se accede con `reserva.ficha`.

La relación 1:N permite registrar varias solicitudes de atención para una reserva. Cada solicitud pertenece a una sola reserva; se consultan con `reserva.solicitudes.all()`.

La relación N:M permite incluir varios platos en una reserva y repetir un plato en distintas reservas. La cantidad y el precio acordado pertenecen al pedido concreto; el precio guardado no cambia al actualizar el menú. `reserva.detalles.all()` y `plato.detalles_reserva.all()` recorren el modelo intermedio. Se impiden platos duplicados en una reserva, cantidades menores que uno y precios negativos.

Se conservan las relaciones CASCADE originales: eliminar Persona elimina sus roles y las reservas del cliente; eliminar Cliente o Mesa elimina sus reservas; eliminar Categoria elimina sus platos. Eliminar un Cliente o Administrador conserva su Persona. Las nuevas relaciones también usan CASCADE: eliminar una reserva elimina su ficha, solicitudes y detalles; eliminar un plato elimina sus detalles. Eliminar un detalle conserva la reserva y el plato.

`reserva_lista` usa `select_related("cliente__persona", "mesa", "ficha")` y `prefetch_related("solicitudes")`. `plato_lista` usa `select_related("categoria")` y `prefetch_related("detalles_reserva__reserva")`. Las plantillas muestran acceso directo, acceso inverso y los atributos del modelo intermedio.

Los formularios y Django Admin ejecutan las validaciones del modelo. Al escribir directamente desde scripts con ORM, llamar a `full_clean()` antes de `save()` para validar reglas como la capacidad; `save()` no lo ejecuta automáticamente. La base de datos protege además el horario único, los estados válidos y la cantidad positiva.

## Instalación y ejecución (PowerShell)

Probado con Python 3.14.4 y Django 6.1.1. Desde esta carpeta, usar el entorno `.venv` existente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver 8010
```

En una copia nueva sin entorno virtual, crearlo primero con `py -3.14 -m venv .venv`.

Abrir http://127.0.0.1:8010/. Para acceder a Django Admin, crear una cuenta:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Se utiliza SQLite (`db.sqlite3`), que no debe borrarse para actualizar el sistema. La migración `0001_initial` se conserva y `0002_reserva_reserva_cantidad_positiva` agrega la restricción de cantidad mayor que cero. Si otra instalación tiene reservas con cantidad cero, deben corregirse antes de aplicar esa migración. `0003_detallereserva_reserva_platos_fichareserva_and_more` incorpora las tres nuevas entidades, la relación N:M y las restricciones de DetalleReserva. Idioma: español; zona horaria: America/Lima. La configuración actual corresponde a desarrollo local.

Las versiones de `requirements.txt` coinciden con los paquetes del entorno local. La ampliación utiliza el ORM de Django y no necesita dependencias adicionales.

## URLs principales

| Página | Ruta |
| --- | --- |
| Inicio | `/` |
| Menú | `/menu/` |
| Filtro de menú | `/menu/?categoria=1` |
| Clientes | `/clientes/` |
| Administradores | `/administradores/` |
| Mesas | `/mesas/` |
| Reservas | `/reservas/` |
| Categorías | `/categorias/` |
| Platos | `/platos/` |
| Detalles de reserva | `/detalles/` |
| Django Admin | `/admin/` |

Cada entidad ofrece `crear/`, `<id>/editar/` y `<id>/eliminar/` bajo su ruta. Cancelación: `/reservas/<id>/cancelar/`. Los nombres siguen `restaurante:<entidad>_lista`, `_crear`, `_editar`, `_eliminar`; la cancelación usa `restaurante:reserva_cancelar`.

## Verificación

Las pruebas cubren CRUD de las seis secciones, creación y edición de Persona con sus roles, rechazo de formularios inválidos, duplicados, capacidad, estados, mesas disponibles, cancelación, eliminación en cascada, filtros del menú, formularios precargados, errores 404 y protección CSRF. Django crea una base temporal para las pruebas y conserva la base de desarrollo.

Se añadieron dos pruebas para DetalleReserva: creación, consulta, edición de cantidad y precio, eliminación sin borrar reserva ni plato, CSRF y rechazo de valores inválidos y duplicados. Ejecutar `manage.py test` para verificar el estado actual antes de publicar.

Los archivos principales son `restaurante/models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `tests.py`, las plantillas de `restaurante/templates/restaurante/` y `restaurante/static/restaurante/estilos.css`.

## Cómo leer el código del curso

Las vistas y rutas están escritas explícitamente para cada entidad. Por ejemplo, para clientes:

1. `restaurante/urls.py` conecta `/clientes/crear/` con `cliente_crear`.
2. `cliente_crear` en `restaurante/views.py` muestra los formularios cuando recibe GET y valida y guarda los datos cuando recibe POST.
3. `PersonaForm`, definido en `restaurante/forms.py`, recoge los datos del cliente. Al crear, se guarda la Persona y se crea el Cliente con dos instrucciones consecutivas. Al editar, solo se guarda la Persona.
4. Después de guardar, se redirige a `cliente_lista`, que consulta los clientes y muestra `cliente_lista.html`.
5. `cliente_editar` carga los datos personales con `instance=cliente.persona`; `cliente_eliminar` muestra la confirmación y solo elimina al recibir POST.

Las otras entidades siguen el mismo patrón con sus propias funciones. No se utiliza un diccionario `SECCIONES` ni se generan rutas automáticamente. Cada listado escribe directamente sus columnas y campos en HTML. Se comparten `base.html`, `lista.html`, `form.html` y `confirmar.html` para reutilizar la presentación.

Se usa un flujo sencillo: validar el formulario, guardar y redirigir. No hay bloques de transacciones, manejo de excepciones ni decoradores de métodos HTTP en las vistas. Si falla el segundo guardado de un cliente o administrador, el primero no se revierte automáticamente.
