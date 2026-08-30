# Barbería - Sistema de gestión de citas

Aplicación web académica desarrollada con Django para organizar las citas de una barbería. El proyecto utiliza el patrón MVT y almacena las reservas temporalmente en memoria, sin utilizar una base de datos para la aplicación de citas.

## Integrantes y distribución de ejercicios

Fabián Ramírez:

- Ejercicio 1: investigar una problemática real.
- Ejercicio 2: capturar los requisitos.
- Ejercicio 3: diseñar el modelo de datos.
- Ejercicio 4: crear la nueva App.
- Ejercicio 5: implementar el Model con datos estáticos.
- Ejercicio 6: implementar el listado con View, URL y Template.

Oscar Eneque:

- Ejercicio 7: implementar el formulario con Forms.
- Ejercicio 8: implementar la vista de creación.
- Ejercicio 9: verificar y documentar el flujo completo.
- Ejercicio 10: actualizar la documentación y publicar el proyecto en GitHub.

## Problemática

Una barbería puede tener dificultades para organizar las citas de sus clientes cuando atiende a varias personas durante el día. Si las reservas se anotan manualmente, pueden producirse cruces de horarios, olvidos o confusiones sobre qué barbero debe atender cada cita. Esta aplicación permite consultar los horarios disponibles, registrar una cita y cancelar una reserva. El sistema puede ser utilizado por los clientes y por el personal de la barbería.

## Requisitos funcionales

1. RF01 - Seleccionar la fecha de la cita: el sistema debe permitir al cliente seleccionar la fecha en la que desea realizar su reserva.

2. RF02 - Consultar horarios disponibles: el sistema debe mostrar los horarios correspondientes a la fecha seleccionada.

3. RF03 - Visualizar el estado de los horarios: el sistema debe permitir identificar cuáles horarios están disponibles y cuáles están ocupados.

4. RF04 - Registrar una cita: el sistema debe permitir registrar una cita ingresando el nombre del cliente y seleccionando un horario disponible.

5. RF05 - Asignar automáticamente el barbero: el sistema debe identificar y asignar el barbero correspondiente al horario seleccionado.

6. RF06 - Evitar reservas duplicadas: el sistema debe impedir que un horario ocupado sea reservado nuevamente en la misma fecha.

7. RF07 - Validar los datos de la reserva: el sistema debe comprobar que el nombre, la fecha y el horario hayan sido ingresados correctamente antes de registrar la cita.

8. RF08 - Cancelar una cita: el sistema debe permitir cancelar una cita registrada y hacer que su horario vuelva a estar disponible.

## Aplicación creada

La aplicación se llama `citas` y contiene la funcionalidad relacionada con la consulta, registro y cancelación de citas.

La entidad principal es Cita y contiene los siguientes datos:

- Nombre del cliente, de tipo string y obligatorio.
- Fecha, de tipo string y obligatoria.
- Horario, de tipo string y obligatorio.
- Horario visible, de tipo string y obligatorio.
- Barbero, de tipo string y obligatorio. Es asignado automáticamente por el sistema.

## Horarios de atención

La barbería trabaja todos los días desde las 10:00 a. m. hasta las 10:00 p. m. y cuenta con tres barberos.

- Barbero 1: desde las 10:00 a. m. hasta las 2:00 p. m.
- Barbero 2: desde las 2:00 p. m. hasta las 6:00 p. m.
- Barbero 3: desde las 6:00 p. m. hasta las 10:00 p. m.

Cada barbero tiene cuatro horarios consecutivos de una hora. Los horarios no son simultáneos y cada uno pertenece a un solo barbero.

## Estructura principal

```text
barberia-project/
|-- manage.py
|-- requirements.txt
|-- README.md
|-- config/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
`-- citas/
    |-- apps.py
    |-- forms.py
    |-- models.py
    |-- urls.py
    |-- views.py
    |-- static/citas/estilos.css
    `-- templates/citas/
        |-- base.html
        |-- lista.html
        `-- reservar.html
```

## Patrón MVT

- Model: `citas/models.py` contiene la lista de horarios y la lista temporal de citas.
- View: `citas/views.py` procesa las solicitudes, valida los datos y consulta o modifica las listas.
- Template: los archivos de `citas/templates/citas/` generan las páginas HTML que ve el usuario.
- URL: `config/urls.py` conecta el proyecto con `citas/urls.py`, donde se encuentran las rutas de la aplicación.
- Form: `citas/forms.py` contiene formularios creados con `forms.Form`.

## Almacenamiento temporal

Las citas se almacenan en una lista de diccionarios llamada `citas`, ubicada en `citas/models.py`. No se utiliza un modelo de base de datos, `ModelForm` ni migraciones para las citas.

Los registros nuevos se pierden cuando se detiene o reinicia el servidor. Este comportamiento es esperado para el laboratorio.

## Flujo de la aplicación

1. El usuario ingresa al listado de citas.
2. Selecciona una fecha.
3. El sistema muestra los horarios disponibles y ocupados.
4. El usuario abre el formulario de reserva.
5. Ingresa su nombre y selecciona un horario disponible.
6. El formulario envía los datos mediante POST.
7. La vista valida los datos y comprueba que el horario no esté ocupado.
8. El sistema identifica automáticamente al barbero.
9. La cita se agrega a la lista temporal.
10. El usuario regresa al listado y observa el horario como ocupado.
11. Si cancela la cita, esta se elimina de la lista y el horario vuelve a estar disponible.

El recorrido técnico es: Request → URL → View → Model → Template → Response.

## Instalación y ejecución

Desde PowerShell, ingresar a la carpeta del proyecto:

```powershell
cd C:\Users\fabia\Desktop\Django\Sem-2\barberia-project
```

Crear un entorno virtual si todavía no existe:

```powershell
python -m venv .venv
```

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Comprobar el proyecto:

```powershell
python manage.py check
```

Iniciar el servidor en el puerto 8001:

```powershell
python manage.py runserver 8001
```

Abrir la aplicación en el navegador:

```text
http://127.0.0.1:8001/citas/
```

El puerto 8001 se utiliza porque el puerto 8000 puede estar ocupado por otro proyecto local.
