# Semana 6: herencia y reutilización de plantillas

## Auditoría

El proyecto ya contaba con `restaurante/templates/restaurante/base.html`, que define encabezado, navegación, pie y bloque `contenido`. Los formularios, confirmaciones, inicio y menú ya heredaban de esa base. Los listados específicos heredaban de `lista.html`, que a su vez hereda de `base.html`; por tanto, las siete pantallas de listado ya compartían la estructura común antes de esta práctica. Se conservaron las vistas y rutas públicas.

La investigación del restaurante tiene diez entidades (Persona, Cliente, Administrador, Mesa, Reserva, Categoria, Plato, FichaReserva, SolicitudReserva y DetalleReserva), más CRUD público para seis secciones principales y para DetalleReserva. Persona se administra a través de Cliente y Administrador; FichaReserva y SolicitudReserva se muestran relacionadas a Reserva y no tienen CRUD público propio.

## Respuestas y evidencia por ejercicio

1. **Auditoría de plantillas:** los listados de clientes, administradores, mesas, reservas, categorías, platos y detalles ya extendían `lista.html`; este extendía `base.html`. Formulario, confirmación, inicio y menú extendían directamente `base.html`. Captura el árbol de plantillas y el inicio de `reserva_lista.html` y `lista.html` en VS Code.
2. **Base común:** `base.html` ya existía con encabezado, menú, pie y bloque `contenido`; se reutilizó como base común. Captura `<header>`, `{% block contenido %}` y `<footer>`.
3. **Migración de una plantilla:** `reserva_lista.html` hereda de `lista.html`, que hereda de `base.html`. Captura las etiquetas `extends` y `block`, y luego `/reservas/` renderizada.
4. **Migración de más plantillas:** los siete listados de entidad usan la misma cadena de herencia; `form.html` también hereda directamente de la base. Captura `cliente_lista.html`, `plato_lista.html` y `/platos/` o `/clientes/` en el navegador.
5. **Filtro:** `reserva_lista.html` formatea la fecha con `date:"d/m/Y"`; `plato_lista.html` muestra el nombre con `upper`; los importes continúan usando `floatformat:2`. Captura una fila visible en `/reservas/` o `/platos/` y resalta la expresión del filtro en VS Code.
6. **Comentario:** `plato_lista.html` contiene un comentario de plantilla que explica por qué el nombre del plato se muestra en mayúsculas. Captura el comentario y la expresión `upper`.
7. **Include, Parte 1:** `_acciones_crud.html` reúne los enlaces Editar y Eliminar y se incluye desde seis listados. Captura el archivo parcial y una invocación `{% include %}` en `cliente_lista.html`.
8. **Autoescape y comparación con Admin:** el autoescape de Django sigue activo; la refactorización no usa `safe` ni desactiva el escape. Para la evidencia, escribe `<script>alert('prueba')</script>` en un campo de texto, abre una vista que muestre ese valor y captura el código fuente donde aparezca escapado como `&lt;script&gt;`. Comprueba la respuesta HTML de una plantilla Django. Las plantillas propias dan una interfaz pública adaptada al restaurante; Admin proporciona gestión autenticada para personal.
9. **Auditoría de investigación:** hay diez entidades en el dominio; Reserva y Plato son buenos ejemplos porque Reserva muestra ficha y solicitudes y Plato muestra categoría y detalles de pedidos. Captura `/reservas/` con ficha/solicitudes visibles y `/platos/` con pedidos si hay registros.
10. **Resto de plantillas:** los listados públicos ya heredan de la base a través de `lista.html`; formularios y confirmaciones también la heredan. No se movieron rutas a `/admin/`. Captura la URL pública `/reservas/` o `/platos/` junto al contenido.
11. **Include en investigación:** `_acciones_crud.html` se reutiliza entre seis plantillas. Captura dos invocaciones, por ejemplo en `cliente_lista.html` y `mesa_lista.html`, además del parcial.
12. **Seguridad:** repite la prueba desde un formulario propio usando un campo de texto, como nombre de categoría o plato, y comprueba en el código fuente de la respuesta que `<` y `>` aparecen como `&lt;` y `&gt;`. Captura el código fuente escapado; borra el valor de prueba después.
13. **Flujo completo y comparación:** recorre crear, listar, editar y eliminar en las pantallas de Reserva y Plato con registros de prueba, y confirma sus relaciones en los listados. Captura cada operación y su URL pública. Las vistas propias conservan rutas públicas y muestran el flujo del restaurante; Admin concentra la gestión interna y exige permisos.
14. **Publicación:** `README.md` enlaza esta guía y `requirements.txt` documenta que la refactorización no agrega dependencias; Django sigue fijado a la versión ya usada por el proyecto. Después de revisar la evidencia, haz commit y push desde una sesión GitHub autenticada. Captura README, `requirements.txt`, página del repositorio y commit publicado.

## Justificación

La herencia mantiene encabezado, navegación y pie en un solo lugar, y hace que las pantallas públicas compartan una presentación consistente. El parcial de acciones evita duplicar enlaces de edición y eliminación. Los filtros mejoran la lectura de fechas, precios y nombres. Django escapa por defecto los valores insertados en el HTML, lo que reduce el riesgo de que texto ingresado por usuarios se interprete como código. Django Admin resuelve la gestión interna autenticada, mientras que estas vistas conservan una experiencia pública y rutas propias para el flujo del restaurante.

## Guía rápida de capturas

- **Código antes/después:** el documento solicita ambos estados. El estado inicial se obtiene de una copia o historial previo; no reconstruirlo cambiando archivos del proyecto.
- **Código final:** `base.html`, `lista.html`, `reserva_lista.html`, `plato_lista.html`, `cliente_lista.html` y `_acciones_crud.html`.
- **Navegador:** `/`, `/reservas/`, `/platos/`, `/reservas/crear/` y las rutas de edición/eliminación de registros de prueba.
- **Autoescape:** código fuente HTML de una respuesta pública con el valor de prueba escapado, sin ejecutar el script.
- **GitHub:** repositorio y commit una vez publicados por el estudiante.

No incluir claves, cookies de sesión ni datos personales reales en las capturas.
