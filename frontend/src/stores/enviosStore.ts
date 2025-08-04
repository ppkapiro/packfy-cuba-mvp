// 🎯 Store de Envíos - Zustand  
// Gestión de estado para envíos y notificaciones

import { create } from 'zustand'
import { enviosAPI } from '../services/api'
import toast from 'react-hot-toast'

export interface Envio {
  id: string
  numero_guia: string
  remitente_nombre: string
  destinatario_nombre: string
  estado_actual: string
  fecha_creacion: string
  fecha_estimada_entrega: string | null
}

interface EnviosState {
  // Estado
  envios: Envio[]
  isLoading: boolean
  error: string | null
  
  // Acciones
  fetchEnvios: () => Promise<void>
  createEnvio: (envioData: any) => Promise<Envio>
  clearError: () => void
  setLoading: (loading: boolean) => void
}

export const useEnviosStore = create<EnviosState>((set) => ({
  // Estado inicial
  envios: [],
  isLoading: false,
  error: null,

  // Cargar envíos
  fetchEnvios: async () => {
    set({ isLoading: true, error: null })
    
    try {
      const response = await enviosAPI.getAll()
      set({ 
        envios: response.data.results || response.data,
        isLoading: false 
      })
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Error al cargar envíos',
        isLoading: false 
      })
      toast.error('Error al cargar envíos')
    }
  },

  // Crear envío
  createEnvio: async (envioData: any) => {
    set({ isLoading: true, error: null })
    
    try {
      const response = await enviosAPI.create(envioData)
      const nuevoEnvio = response.data
      
      // Actualizar la lista de envíos
      set(state => ({
        envios: [nuevoEnvio, ...state.envios],
        isLoading: false
      }))
      
      toast.success('¡Envío creado exitosamente!')
      return nuevoEnvio
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Error al crear envío'
      set({ 
        error: errorMessage,
        isLoading: false 
      })
      toast.error(errorMessage)
      throw error
    }
  },

  // Limpiar error
  clearError: () => {
    set({ error: null })
  },

  // Establecer loading
  setLoading: (loading: boolean) => {
    set({ isLoading: loading })
  }
}))
