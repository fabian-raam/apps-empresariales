import { useState } from 'react'
import './App.css'

const nombreAplicacion = 'Restaurante La Mesa'
const impuesto = 0.18

// Datos escritos a mano con la misma forma que /api/platos/ de Semana 8.
const platos = [
  { plato_id: 1, categoria: 1, nombre: 'Sopa criolla', precio: '15.00', existencias: 0, img_url: '' },
  { plato_id: 2, categoria: 2, nombre: 'Arroz con pollo', precio: '22.50', existencias: 3, img_url: '' },
  { plato_id: 3, categoria: 2, nombre: 'Lomo saltado', precio: '29.90', existencias: 12, img_url: '' },
  { plato_id: 4, categoria: 3, nombre: 'Torta de chocolate', precio: '12.00', existencias: 4, img_url: '' },
  { plato_id: 5, categoria: 1, nombre: 'Ensalada fresca', precio: '16.50', existencias: 9, img_url: '' },
]

// Forma basada en /api/reservas/: detalles incluye el modelo intermedio y el plato.
const reservas = [
  {
    reserva_id: 101,
    cliente: { cliente_id: 1, persona: { nombres: 'Ana', apellidos: 'Pérez' } },
    mesa: 4,
    fecha: '2026-10-18',
    hora: '13:00:00',
    cantidad_personas: 2,
    estado: 'confirmada',
    ficha: { ocasion: 'Almuerzo familiar', observaciones: '' },
    solicitudes: [{ descripcion: 'Silla para niño', atendida: true }],
    detalles: [
      { detalle_id: 1001, plato: { plato_id: 2, nombre: 'Arroz con pollo', precio: '22.50' }, cantidad: 2, precio_unitario: '22.50' },
      { detalle_id: 1002, plato: { plato_id: 4, nombre: 'Torta de chocolate', precio: '12.00' }, cantidad: 1, precio_unitario: '12.00' },
    ],
  },
  {
    reserva_id: 102,
    cliente: { cliente_id: 2, persona: { nombres: 'Luis', apellidos: 'Torres' } },
    mesa: 2,
    fecha: '2026-10-18',
    hora: '14:30:00',
    cantidad_personas: 3,
    estado: 'pendiente',
    ficha: null,
    solicitudes: [],
    detalles: [
      { detalle_id: 1003, plato: { plato_id: 3, nombre: 'Lomo saltado', precio: '29.90' }, cantidad: 2, precio_unitario: '28.00' },
    ],
  },
]

function precioConImpuesto(precio) {
  return (precio * (1 + impuesto)).toFixed(2)
}

function totalReserva(detalles) {
  return detalles.reduce(
    (total, detalle) => total + Number(detalle.precio_unitario) * detalle.cantidad,
    0,
  )
}

function App() {
  const [mostrarVacio, setMostrarVacio] = useState(false)
  const platosVisibles = mostrarVacio ? [] : platos

  return (
    <main className="app">
      <header className="encabezado">
        <p className="etiqueta">Semana 9 · Interfaz React</p>
        <h1>{nombreAplicacion}</h1>
        <p className="introduccion">
          Menú y reservas de ejemplo. Los datos están escritos en arreglos y todavía no se leen desde la API.
        </p>
        {platosVisibles.length > 0 && (
          <p className="precio-impuesto">
            Ejemplo con IGV: S/ {precioConImpuesto(Number(platosVisibles[0].precio))}
          </p>
        )}
      </header>

      <section className="seccion" aria-labelledby="titulo-platos">
        <div className="titulo-seccion">
          <div>
            <p className="etiqueta">Datos de Plato</p>
            <h2 id="titulo-platos">Nuestro menú</h2>
          </div>
          <button
            className="boton-secundario"
            type="button"
            onClick={() => setMostrarVacio((vacio) => !vacio)}
          >
            {mostrarVacio ? 'Volver a mostrar platos' : 'Probar lista vacía'}
          </button>
        </div>

        {platosVisibles.length === 0 ? (
          <p className="mensaje-vacio">No hay registros de platos.</p>
        ) : (
          <ul className="rejilla-platos">
            {platosVisibles.map((plato) => (
              <li className="tarjeta-plato" key={plato.plato_id}>
                <div className="tarjeta-cabecera">
                  <span className="id-registro">Plato #{plato.plato_id}</span>
                  <span className="precio">S/ {Number(plato.precio).toFixed(2)}</span>
                </div>
                <h3>{plato.nombre}</h3>
                <p
                  className={plato.existencias === 0 ? 'estado agotado' : 'estado disponible'}
                  style={{ fontWeight: plato.existencias < 5 ? 700 : 500 }}
                >
                  {plato.existencias === 0
                    ? 'Agotado'
                    : `Stock: ${plato.existencias} unidades`}
                </p>
                {plato.existencias > 0 && plato.existencias < 5 && (
                  <p className="ultimas-unidades">¡Quedan pocas unidades!</p>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="seccion" aria-labelledby="titulo-reservas">
        <div className="titulo-seccion">
          <div>
            <p className="etiqueta">Datos de Reserva y DetalleReserva</p>
            <h2 id="titulo-reservas">Reservas recientes</h2>
          </div>
          <span className="contador">{reservas.length} reservas</span>
        </div>

        <ul className="lista-reservas">
          {reservas.map((reserva) => (
            <li className="tarjeta-reserva" key={reserva.reserva_id}>
              <div className="tarjeta-cabecera">
                <div>
                  <span className="id-registro">Reserva #{reserva.reserva_id}</span>
                  <h3>{reserva.cliente.persona.nombres} {reserva.cliente.persona.apellidos}</h3>
                </div>
                <span className={`insignia estado-${reserva.estado}`}>
                  {reserva.estado}
                </span>
              </div>
              <p className="detalle-reserva">
                Mesa {reserva.mesa} · {reserva.fecha} · {reserva.hora} · {reserva.cantidad_personas} personas
              </p>
              <ul className="lista-detalles">
                {reserva.detalles.map((detalle) => (
                  <li key={detalle.detalle_id}>
                    <span>{detalle.cantidad} × {detalle.plato.nombre}</span>
                    <span>S/ {(Number(detalle.precio_unitario) * detalle.cantidad).toFixed(2)}</span>
                  </li>
                ))}
              </ul>
              <p className="total-reserva">
                Total de la reserva: S/ {totalReserva(reserva.detalles).toFixed(2)}
              </p>
            </li>
          ))}
        </ul>
      </section>

      <footer className="pie">
        React muestra los datos. La conexión con Django REST se realizará en una semana posterior.
      </footer>
    </main>
  )
}

export default App
