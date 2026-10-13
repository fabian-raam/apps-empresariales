# Semana 8: API REST con Django REST Framework

La práctica expone por JSON los mismos modelos del restaurante, sin sustituir sus páginas HTML ni su ORM. Se instalaron Django REST Framework 3.18.3 y sus herramientas en `INSTALLED_APPS`; esta versión declara soporte para Django 6.1, que es la versión de este proyecto. No se agregan modelos ni migraciones.

El recurso simple principal es `Plato`, con validación de precio mayor que cero. También se exponen `Categoria` y `Mesa` con CRUD. `Reserva` se ofrece en modo de solo lectura y presenta cliente/persona, ficha, solicitudes y detalles con el plato anidado. Se usan los modelos existentes y el `ReservaQuerySet` de Semana 7.

## Archivos añadidos o modificados

- `config/settings.py`: agrega `rest_framework` a `INSTALLED_APPS`.
- `requirements.txt`: fija `djangorestframework==3.18.3`.
- `restaurante/serializers.py`: `PlatoSerializer`, `CategoriaSerializer`, `MesaSerializer` y serializers anidados de reserva. `PlatoSerializer.validate_precio()` impide precio cero o negativo.
- `restaurante/api_views.py`: tres `ModelViewSet` CRUD (plato, categoría y mesa) y `ReservaReadOnlyViewSet`.
- `restaurante/api_urls.py`: registra los ViewSets en `DefaultRouter`.
- `config/urls.py`: monta el router bajo `/api/`.
- `restaurante/test_api.py`: prueba serialización, validación, CRUD, estados HTTP, filtros, acción, datos anidados y optimización de consultas.

## Recursos y rutas

| Ruta | Vista | Métodos |
| --- | --- | --- |
| `/api/` | índice del router | GET |
| `/api/platos/` y `/api/platos/<id>/` | `PlatoViewSet` | GET, POST, PUT, PATCH, DELETE |
| `/api/categorias/` y `/api/categorias/<id>/` | `CategoriaViewSet` | GET, POST, PUT, PATCH, DELETE |
| `/api/mesas/` y `/api/mesas/<id>/` | `MesaViewSet` | GET, POST, PUT, PATCH, DELETE |
| `/api/reservas/` y `/api/reservas/<id>/` | `ReservaReadOnlyViewSet` | GET |
| `/api/reservas/mes-actual/` | acción `mes_actual` | GET |

El router crea las rutas CRUD a partir de los `ModelViewSet`. La API navegable de DRF sirve para inspeccionar y enviar solicitudes desde el navegador.

## Ejercicios y ejemplos

### Parte 1

1. **Instalación y recursos:** el recurso simple es Plato; el relacionado es Reserva. Reserva conserva el estado y el QuerySet personalizado de Semana 7.
2. **Serializar:** en el shell de Django:

   ```python
   from restaurante.models import Plato
   from restaurante.serializers import PlatoSerializer
   plato = Plato.objects.first()
   PlatoSerializer(plato).data
   PlatoSerializer(Plato.objects.all(), many=True).data
   ```

   `many=True` indica al serializer que recibe una colección de objetos, no un único objeto.
3. **Validar y guardar:** probar precio válido e inválido:

   ```python
   from restaurante.models import Categoria
   from restaurante.serializers import PlatoSerializer
   categoria = Categoria.objects.first()
   valido = PlatoSerializer(data={"categoria": categoria.pk, "nombre": "Plato API válido", "precio": "12.50", "existencias": 5, "img_url": ""})
   valido.is_valid(), valido.validated_data
   plato = valido.save()
   invalido = PlatoSerializer(data={"categoria": categoria.pk, "nombre": "Plato API inválido", "precio": "0.00", "existencias": 5, "img_url": ""})
   invalido.is_valid(), invalido.errors
   ```

4. **Vistas genéricas:** el ejercicio presenta primero `ListCreateAPIView` y `RetrieveUpdateDestroyAPIView`; en el resultado final fueron reemplazadas por el ViewSet y router del ejercicio 5.
5. **ViewSet y router:** `PlatoViewSet` genera las rutas CRUD y `/api/` las enumera. Las operaciones provienen de las acciones estándar de `ModelViewSet`.
6. **Códigos HTTP:** se verificaron con `APITestCase` en `test_api.py`:

   | Solicitud | Resultado |
   | --- | --- |
   | GET lista / GET detalle | 200 |
   | POST válido | 201 |
   | POST precio no válido | 400 |
   | PATCH | 200 |
   | GET ID inexistente | 404 |
   | DELETE | 204 |

   La API devuelve JSON y códigos HTTP para que otros programas procesen la respuesta; un Template devuelve una página HTML para mostrarla directamente. Los ViewSets usan `AllowAny`: la API está abierta y todavía necesita autenticación y permisos antes de un despliegue real.
7. **Relaciones anidadas:** `ReservaReadSerializer` incluye cliente/persona, ficha, solicitudes y detalles con el plato. `ReservaReadOnlyViewSet.get_queryset()` precarga esas relaciones. Ejemplo de medición en shell:

   ```python
   from django.db import connection, reset_queries
   from restaurante.models import Reserva
   from restaurante.serializers import ReservaReadSerializer
   reset_queries()
   ReservaReadSerializer(Reserva.objects.all(), many=True).data
   print("Antes:", len(connection.queries))
   reset_queries()
   qs = Reserva.objects.select_related("cliente__persona", "mesa", "ficha").prefetch_related("solicitudes", "detalles__plato")
   ReservaReadSerializer(qs, many=True).data
   print("Después:", len(connection.queries))
   ```

   Con la base local preparada, la prueba dio **45 consultas antes y 4 después**. La cantidad puede cambiar si se modifica el número de reservas o detalles.

8. **Búsqueda, orden y acción:** ejemplos:

   - `/api/platos/?search=sopa`
   - `/api/platos/?ordering=-precio`
   - `/api/platos/?search=sopa&ordering=precio`
   - `/api/reservas/?estado=confirmada&mes=actual`
   - `/api/reservas/mes-actual/`

   Plato usa `SearchFilter` y `OrderingFilter`. Reserva filtra por `estado` y `mes`; su acción `mes-actual` reutiliza `del_mes_actual()` del QuerySet.

### Parte 2: investigación propia

Este repositorio tiene una aplicación de restaurante, por lo que los recursos anteriores cubren también la práctica de investigación: Plato, Categoria y Mesa tienen ModelSerializer; Plato y Categoria/Mesa están expuestos con ModelViewSet; Reserva proporciona la lectura anidada, el filtro y la acción. Si la investigación propia se encuentra en otro proyecto, será necesario trasladar estas técnicas a sus modelos.

9. **Equivalencias:** Plato como recurso simple y regla de precio; Reserva como recurso relacionado; `Reserva.estado` como filtro; `del_mes_actual()` como método reutilizado por la acción.
10. **Serializers:** al menos tres ModelSerializer para Plato, Categoria y Mesa; validación propia de precio en Plato.
11. **ViewSets y estados:** ViewSets CRUD registrados para platos, categorías y mesas; los estados esperados están cubiertos por `test_api.py`.
12. **Relaciones:** Reserva de solo lectura entrega relaciones anidadas usando un queryset optimizado.
13. **Filtros y acción:** búsqueda y orden de platos, filtro de reservas por estado/mes y acción de reservas del mes actual.
14. **Publicación:** README y requirements documentan la API y la dependencia. El commit/push corresponde al repositorio indicado por el estudiante.

## Ejecución y comprobación

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver 8010
```

Abrir `http://127.0.0.1:8010/api/`. Los endpoints de escritura no requieren migración porque se apoyan en los modelos existentes.
