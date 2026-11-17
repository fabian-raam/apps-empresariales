# Semana 12 — Parte 1: React consume la API de platos

Esta práctica usa el recurso `Plato` que ya expone Django REST. La interfaz original de la Semana 9 se conserva; desde ella se abre la vista práctica de la Semana 12. React y Django se ejecutan en terminales separadas. La comunicación usa Axios y HTTP, y CORS permite que el navegador acepte la respuesta entre ambos puertos.

## Ejecutar

Terminal 1, desde la raíz `restaurante-project`:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 8010
```

Terminal 2:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Abre `http://localhost:5173/` y pulsa “Abrir práctica Semana 12 (API)”. La URL base predeterminada está en `frontend/src/api.js`. Si Django usa otro puerto, definir `VITE_API_URL`, por ejemplo `http://127.0.0.1:8000/api/`.

## Ejercicio 1 — API y métodos HTTP

El recurso seleccionado es Plato. La lista está en `http://127.0.0.1:8010/api/platos/`. Una petición GET correcta responde HTTP 200 con JSON; `PlatoSerializer` devuelve `plato_id`, `categoria`, `nombre`, `precio`, `existencias` e `img_url`.

| Operación | Método | URL | Respuesta esperada |
| --- | --- | --- | --- |
| Listar | GET | `/api/platos/` | 200 |
| Consultar un plato | GET | `/api/platos/{id}/` | 200; 404 si no existe |
| Crear | POST | `/api/platos/` | 201; 400 si los datos no pasan validación |
| Reemplazar | PUT | `/api/platos/{id}/` | 200; 400 por datos inválidos; 404 si no existe |
| Actualizar parcialmente | PATCH | `/api/platos/{id}/` | 200; 400 por datos inválidos; 404 si no existe |
| Eliminar | DELETE | `/api/platos/{id}/` | 204; 404 si no existe |

La API responde datos JSON y un código HTTP. Un Template de Django, en cambio, recibe datos del servidor y los presenta como una página HTML.

## Ejercicio 2 — CORS

`django-cors-headers` está en `requirements.txt` y `corsheaders` está en `INSTALLED_APPS`. `CorsMiddleware` está antes de `CommonMiddleware`, y `CORS_ALLOWED_ORIGINS` permite `http://localhost:5173` en `config/settings.py`.

CORS es una regla del navegador que controla solicitudes entre orígenes distintos. React usa el origen `localhost:5173`, mientras Django usa `127.0.0.1:8010`. Django autoriza el origen de React mediante la cabecera CORS. Para observar el bloqueo previo solicitado en el enunciado, se debe retirar temporalmente ese origen, reiniciar Django, hacer el `fetch` desde la consola del navegador y luego restaurarlo. No dejar la configuración retirada.

## Ejercicio 3 — Axios

`frontend/src/api.js` crea una instancia Axios con `baseURL` y timeout de diez segundos. Todos los componentes importan esa instancia. Centralizar la dirección facilita cambiar puerto o servidor en un solo lugar.

## Ejercicio 4 — GET con `useEffect`

`frontend/src/practica/ListaPractica.jsx` carga platos con `api.get('platos/')`. El efecto se ejecuta al montar y cada vez que cambia el texto de búsqueda; actualiza el estado con la respuesta y dibuja la lista con `map()` y `key={plato.plato_id}`.

La petición va dentro de `useEffect` porque es una comunicación externa al renderizado. Si estuviera directamente en el cuerpo del componente, se repetiría en cada render. El callback del efecto no es `async`: devuelve una función de limpieza; la petición asíncrona se define dentro de él.

## Ejercicio 5 — Carga, error y lista vacía

La pantalla muestra “Cargando...” mientras espera la respuesta, “No se pudo cargar la lista” cuando Django no responde y un mensaje de lista vacía si la API responde correctamente con cero coincidencias. Para demostrar el error, detener Django mientras la vista está abierta. React conserva una explicación en pantalla en vez de dejar el listado en blanco.

## Ejercicio 6 — POST y validación

El formulario controlado de la práctica envía `categoria`, `nombre`, `precio`, `existencias` e `img_url` con `api.post('platos/', datos)`. Cuando Django devuelve 201, React agrega `response.data` al estado sin volver a pedir la lista.

Para demostrar el 400, enviar precio `0`. `PlatoSerializer.validate_precio` rechaza precios menores o iguales a cero. La respuesta de validación se muestra en pantalla desde `err.response.data`.

## Ejercicio 7 — DELETE y PATCH

Cada fila tiene “Eliminar”. `api.delete('platos/{id}/')` debe devolver 204; entonces React quita el elemento con `filter()`. El botón “+1 stock (PATCH)” envía la nueva existencia con `api.patch(...)`; cuando Django devuelve 200, React reemplaza el registro correspondiente usando `map()`.

## Ejercicio 8 — Búsqueda y flujo

El campo de búsqueda está controlado por el estado `buscar`. Su cambio vuelve a ejecutar el efecto, que llama la API con `{ params: { search: buscar } }`; en Network se observa `/api/platos/?search=...`. El backend ya implementa búsqueda por nombre y nombre de categoría.

En el recorrido, React inicia la acción; Axios hace la petición; el router resuelve `/api/platos/`; `PlatoViewSet` consulta y aplica búsqueda; `PlatoSerializer` valida o convierte los campos; el ORM consulta o modifica la base de datos; Django responde JSON y un código HTTP; React actualiza su estado y vuelve a dibujar la vista. La API usa `AllowAny`, así que no pide inicio de sesión ni permisos de usuario.

Verificación:

```powershell
npm.cmd run lint
npm.cmd run build
```

## Capturas para el documento

1. Terminal con `node -v`, `npm.cmd -v`, Django instalado y Axios en `package.json`.
2. GET `/api/platos/` abierto en el navegador o cliente API con código 200 y fragmento JSON.
3. Configuración CORS en `config/settings.py`; captura de error de origen bloqueado y luego GET exitoso con CORS activo.
4. Código de `frontend/src/api.js` y `package.json`.
5. Código de `ListaPractica.jsx`, página con registros y Network mostrando GET 200.
6. Vista de carga/lista vacía y captura con Django detenido mostrando el error.
7. Formulario y Network para POST 201; luego precio cero con respuesta 400 visible.
8. Network con DELETE 204 y PATCH 200, y la lista antes/después de cada operación.
9. Búsqueda con URL `?search=` y resultados; terminal con `lint` y `build` exitosos.

La Parte 2 del laboratorio —integrar estas acciones en el panel administrativo completo— no forma parte de esta implementación.
