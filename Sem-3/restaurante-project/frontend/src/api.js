import axios from 'axios'

// Centraliza la URL base; puede cambiarse con VITE_API_URL si Django usa otro puerto.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8010/api/',
  timeout: 10000,
})

export default api
