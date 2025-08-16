// 🎯 Store de Envíos - Zustand
// Gestión de estado para envíos y notificaciones

import { create } from "zustand";
import { enviosAPI } from "../services/api";
import toast from "react-hot-toast";

export interface Envio {
  id: string;
  numero_guia: string;
  remitente_nombre: string;
  destinatario_nombre: string;
  estado_actual: string;
  fecha_creacion: string;
  fecha_estimada_entrega: string | null;
}

interface EnviosState {
  // Estado
  envios: Envio[];
  isLoading: boolean;
  error: string | null;

  // Acciones
  fetchEnvios: () => Promise<void>;
  createEnvio: (envioData: any) => Promise<Envio>;
  clearError: () => void;
  setLoading: (loading: boolean) => void;
}

export const useEnviosStore = create<EnviosState>((set) => ({
  // Estado inicial
  envios: [],
  isLoading: false,
  error: null,

  // Cargar envíos
  fetchEnvios: async () => {
    set({ isLoading: true, error: null });
    const response = await enviosAPI.getAll();
    if (response.status >= 200 && response.status < 300) {
      const data: any = response.data;
      set({
        envios: (data && (data.results || data)) || [],
        isLoading: false,
      });
    } else {
      const msg = response.error || "Error al cargar envíos";
      set({ error: msg, isLoading: false });
      toast.error(msg);
    }
  },

  // Crear envío
  createEnvio: async (envioData: any) => {
    set({ isLoading: true, error: null });
    const response = await enviosAPI.create(envioData);
    if (response.status >= 200 && response.status < 300) {
      const nuevoEnvio = response.data as any;
      set((state) => ({
        envios: [nuevoEnvio, ...state.envios],
        isLoading: false,
      }));
      toast.success("¡Envío creado exitosamente!");
      return nuevoEnvio;
    } else {
      const errorMessage = response.error || "Error al crear envío";
      set({ error: errorMessage, isLoading: false });
      toast.error(errorMessage);
      throw new Error(errorMessage);
    }
  },

  // Limpiar error
  clearError: () => {
    set({ error: null });
  },

  // Establecer loading
  setLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },
}));
