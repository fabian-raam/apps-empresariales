import { useEffect, useState } from 'react'
import api from '../api.js'
import './ListaPractica.css'

const formularioInicial = {
  categoria: '',
  nombre: '',
  precio: '',
  existencias: '10',
  img_url: '',
}

function mensajeDeError(error) {
  const respuesta = error.response?.data
  if (respuesta && typeof respuesta === 'object') {
    return Object.entries(respuesta)
      .map(([campo, mensajes]) => {
        const texto = Array.isArray(mensajes) ? mensajes.join(' ') : String(mensajes)
        return campo === 'detail' ? texto : `${campo}: ${texto}`
      })
      .join(' · ')
  }
  return error.message || 'Ocurrió un error al comunicarse con Django.'
}

function ListaPractica({ onVolver }) {
  const [platos, setPlatos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [cargando, setCargando] = useState(true)
  const [errorCarga, setErrorCarga] = useState('')
  const [errorAccion, setErrorAccion] = useState('')
  const [mensaje, setMensaje] = useState('')
  const [buscar, setBuscar] = useState('')
  const [formulario, setFormulario] = useState(formularioInicial)
  const [guardando, setGuardando] = useState(false)

  useEffect(() => {
    let vigente = true

    async function cargarPlatos() {
      setCargando(true)
      setErrorCarga('')
      try {
        const respuesta = await api.get('platos/', {
          params: buscar.trim() ? { search: buscar.trim() } : {},
        })
        if (vigente) setPlatos(respuesta.data)
      } catch (error) {
        if (vigente) setErrorCarga(mensajeDeError(error))
      } finally {
        if (vigente) setCargando(false)
      }
    }

    cargarPlatos()
    return () => {
      vigente = false
    }
  }, [buscar])

  useEffect(() => {
    let vigente = true

    async function cargarCategorias() {
      try {
        const respuesta = await api.get('categorias/')
        if (vigente) setCategorias(respuesta.data)
      } catch (error) {
        if (vigente) setErrorAccion(`No se pudieron cargar las categorías: ${mensajeDeError(error)}`)
      }
    }

    cargarCategorias()
    return () => {
      vigente = false
    }
  }, [])

  function cambiarFormulario(evento) {
    const { name, value } = evento.target
    setFormulario((actual) => ({ ...actual, [name]: value }))
  }

  async function crearPlato(evento) {
    evento.preventDefault()
    setErrorAccion('')
    setMensaje('')
    setGuardando(true)

    const nuevoPlato = {
      ...formulario,
      categoria: Number(formulario.categoria),
      precio: formulario.precio,
      existencias: Number(formulario.existencias),
      img_url: formulario.img_url.trim(),
    }

    try {
      const respuesta = await api.post('platos/', nuevoPlato)
      setPlatos((actuales) => [respuesta.data, ...actuales])
      setFormulario(formularioInicial)
      setMensaje('Plato creado correctamente (HTTP 201).')
    } catch (error) {
      setErrorAccion(`${mensajeDeError(error)}${error.response?.status ? ` (HTTP ${error.response.status})` : ''}`)
    } finally {
      setGuardando(false)
    }
  }

  async function eliminarPlato(platoId) {
    setErrorAccion('')
    setMensaje('')
    try {
      const respuesta = await api.delete(`platos/${platoId}/`)
      if (respuesta.status === 204) {
        setPlatos((actuales) => actuales.filter((plato) => plato.plato_id !== platoId))
        setMensaje(`Plato #${platoId} eliminado (HTTP 204).`)
      }
    } catch (error) {
      setErrorAccion(`${mensajeDeError(error)}${error.response?.status ? ` (HTTP ${error.response.status})` : ''}`)
    }
  }

  async function aumentarExistencias(plato) {
    setErrorAccion('')
    setMensaje('')
    try {
      const respuesta = await api.patch(`platos/${plato.plato_id}/`, {
        existencias: Number(plato.existencias) + 1,
      })
      setPlatos((actuales) => actuales.map((actual) => (
        actual.plato_id === plato.plato_id ? respuesta.data : actual
      )))
      setMensaje(`Existencias de “${plato.nombre}” actualizadas (HTTP 200).`)
    } catch (error) {
      setErrorAccion(`${mensajeDeError(error)}${error.response?.status ? ` (HTTP ${error.response.status})` : ''}`)
    }
  }

  return (
    <main className="practica">
      <div className="practica-barra">
        <button className="practica-volver" type="button" onClick={onVolver}>
          Volver al menú de Semana 9
        </button>
        <span>Semana 12 · Práctica de API</span>
      </div>

      <header className="practica-encabezado">
        <p className="practica-etiqueta">React + Axios + Django REST</p>
        <h1>Gestión de platos</h1>
        <p>Esta pantalla consulta y modifica datos reales de Django mediante la API REST.</p>
      </header>

      <section className="practica-panel" aria-labelledby="buscar-platos">
        <label htmlFor="buscar-platos">Buscar por nombre o categoría</label>
        <input
          id="buscar-platos"
          type="search"
          value={buscar}
          onChange={(evento) => setBuscar(evento.target.value)}
          placeholder="Escribe para buscar..."
        />
        <p className="practica-ayuda">La búsqueda se envía a la API como el parámetro ?search=.</p>
      </section>

      <section className="practica-panel" aria-labelledby="crear-plato">
        <h2 id="crear-plato">Crear un plato</h2>
        <p className="practica-ayuda">Para probar el error de validación, envía un precio igual a 0.</p>
        <form className="practica-formulario" onSubmit={crearPlato}>
          <label>
            Categoría
            <select name="categoria" value={formulario.categoria} onChange={cambiarFormulario} required>
              <option value="">Elige una categoría</option>
              {categorias.map((categoria) => (
                <option key={categoria.categoria_id} value={categoria.categoria_id}>
                  {categoria.nombre}
                </option>
              ))}
            </select>
          </label>
          <label>
            Nombre
            <input name="nombre" value={formulario.nombre} onChange={cambiarFormulario} maxLength="100" required />
          </label>
          <label>
            Precio
            <input name="precio" type="number" step="0.01" value={formulario.precio} onChange={cambiarFormulario} required />
          </label>
          <label>
            Existencias
            <input name="existencias" type="number" min="0" step="1" value={formulario.existencias} onChange={cambiarFormulario} required />
          </label>
          <label className="practica-campo-ancho">
            URL de imagen (opcional)
            <input name="img_url" type="url" value={formulario.img_url} onChange={cambiarFormulario} />
          </label>
          <button className="practica-primario" type="submit" disabled={guardando || categorias.length === 0}>
            {guardando ? 'Guardando…' : 'Crear plato'}
          </button>
        </form>
      </section>

      {mensaje && <p className="practica-aviso practica-exito" role="status">{mensaje}</p>}
      {errorAccion && <p className="practica-aviso practica-error" role="alert">{errorAccion}</p>}

      <section className="practica-panel" aria-labelledby="lista-platos-api">
        <div className="practica-lista-titulo">
          <h2 id="lista-platos-api">Platos recibidos desde Django</h2>
          <span>{platos.length} registros</span>
        </div>
        {cargando && <p role="status">Cargando...</p>}
        {!cargando && errorCarga && (
          <div className="practica-vacio practica-error" role="alert">
            <p>No se pudo cargar la lista.</p>
            <p>{errorCarga}</p>
            <p className="practica-ayuda">Comprueba que Django esté ejecutándose en el puerto 8010.</p>
          </div>
        )}
        {!cargando && !errorCarga && platos.length === 0 && (
          <p className="practica-vacio">No hay registros que coincidan con la búsqueda.</p>
        )}
        {!cargando && !errorCarga && platos.length > 0 && (
          <div className="practica-tabla-contenedor">
            <table className="practica-tabla">
              <thead>
                <tr><th>ID</th><th>Plato</th><th>Precio</th><th>Existencias</th><th>Acciones</th></tr>
              </thead>
              <tbody>
                {platos.map((plato) => (
                  <tr key={plato.plato_id}>
                    <td>#{plato.plato_id}</td>
                    <td>{plato.nombre}</td>
                    <td>S/ {Number(plato.precio).toFixed(2)}</td>
                    <td>{plato.existencias}</td>
                    <td className="practica-acciones">
                      <button type="button" onClick={() => aumentarExistencias(plato)}>
                        +1 stock (PATCH)
                      </button>
                      <button className="practica-eliminar" type="button" onClick={() => eliminarPlato(plato.plato_id)}>
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  )
}

export default ListaPractica
