# Semana 9: primera interfaz con React

## Objetivo

Crear una interfaz separada de Django con React y Vite. En esta semana se practican JSX, arreglos, expresiones de JavaScript, renderizado condicional, `map()`, relaciones anidadas y estilos. La interfaz usa datos de ejemplo escritos en el código: todavía no consulta la API REST.

## Preparar y ejecutar

Se requiere Node.js 20.19 o superior, o 22.12 o superior. En Windows PowerShell, si la política bloquea `npm`, usar `npm.cmd`:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Vite muestra una dirección local, normalmente `http://localhost:5173/`. Para revisar las reglas y generar la versión compilada:

```powershell
npm.cmd run lint
npm.cmd run build
```

`node_modules/` y `dist/` están excluidos de Git en `frontend/.gitignore`.

## Ejercicio 1: entorno React con Vite

La aplicación vive en `frontend/`, junto al proyecto Django. `package.json` declara las dependencias y comandos; `package-lock.json` fija sus versiones. `index.html` contiene el elemento raíz, `src/main.jsx` inicia React y `src/App.jsx` presenta la pantalla.

Equivalencias para ubicarse: `npm` administra dependencias como `pip`; `package.json` describe el proyecto JavaScript como `requirements.txt` describe dependencias Python; `node_modules/` contiene paquetes instalados como un entorno virtual; `npm run dev` inicia Vite y `manage.py runserver` inicia Django.

## Ejercicio 2: JSX y expresiones

En `src/App.jsx`, `nombreAplicacion` se muestra dentro de JSX con `{nombreAplicacion}`. La función `precioConImpuesto()` calcula el precio más el 18 % y el resultado se presenta en la página. Las expresiones entre llaves permiten insertar valores y resultados de JavaScript en la interfaz.

## Ejercicio 3: arreglos y renderizado de platos

El arreglo `platos` contiene cinco objetos con campos representativos de la respuesta de `/api/platos/`: identificador, categoría, nombre, precio, existencias e imagen. `platosVisibles.map(...)` crea una tarjeta por cada objeto. `key={plato.plato_id}` ayuda a React a identificar cada elemento de la lista. El precio se formatea con `toFixed(2)`.

## Ejercicio 4: condiciones

El operador ternario muestra “Agotado” cuando las existencias son cero y la cantidad de unidades en caso contrario. El operador `&&` muestra el aviso de pocas unidades si el stock está entre una y cuatro. Otro ternario elige entre el mensaje de lista vacía y el listado.

El botón “Probar lista vacía” usa `useState` para alternar la lista visible entre los cinco platos y un arreglo vacío. Así se puede comprobar el estado vacío sin modificar los datos de ejemplo.

## Ejercicio 5: relaciones y arreglos anidados

El arreglo `reservas` representa dos reservas. Cada una contiene datos de cliente y un arreglo `detalles`; cada detalle incluye un plato, una cantidad y un precio unitario. Un primer `map()` muestra reservas y otro, dentro de este, muestra sus platos. Cada elemento tiene una clave única.

`totalReserva()` usa `reduce()` para multiplicar el precio unitario por la cantidad y sumar los detalles de una reserva. El modelo intermedio representado es `DetalleReserva`, que relaciona una reserva con cada plato pedido.

## Ejercicio 6: clases y estilos

Los elementos JSX utilizan `className` para conectar componentes con reglas de `src/App.css`. El estado del plato también tiene un estilo en línea: el peso de la letra cambia según las existencias. `src/index.css` queda vacío para que la presentación de esta pantalla se defina en `App.css`.

## Entidades y relación usadas

La entidad principal del menú es `Plato`; la otra entidad principal es `Reserva`. La relación de muchos platos por reserva se representa mediante `DetalleReserva`, que además guarda cantidad y precio unitario. Los objetos son ejemplos con forma compatible con datos de la API de Semana 8, adaptados para mostrarse en React. No se realizan solicitudes HTTP ni se guardan cambios en Django.

## Capturas sugeridas

1. Vista del menú con las cinco tarjetas, que evidencia el arreglo, `map()` y el formato del precio.
2. Vista de una tarjeta agotada y otra con pocas existencias, que evidencia las condiciones.
3. Interfaz tras pulsar “Probar lista vacía”, que muestra el mensaje condicional.
4. Sección de reservas con los detalles de platos y el total, que evidencia los arreglos anidados y `reduce()`.
5. Terminal con `npm.cmd run lint` y `npm.cmd run build` finalizados correctamente.

## Resultado

La semana introduce React como capa de presentación y JavaScript como fuente de datos temporal. La conexión con la API de Django queda para una actividad posterior.
