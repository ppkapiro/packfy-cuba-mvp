// 🎯 Store de Autenticación - Zustand
// Gestión de estado moderna y simple

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { authAPI } from "../services/api";

export interface User {
  id: string;
  email: string;
  nombre: string;
  apellidos: string;
  es_administrador_empresa: boolean;
}

interface AuthState {
  // Estado
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  // Acciones
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Estado inicial
      user: null,
      token: null,
      isLoading: false,
      isAuthenticated: false,

      // Acción de login
      login: async (email: string, password: string) => {
        set({ isLoading: true });

        try {
          const response = await authAPI.login(email, password);

          if (response.error) {
            throw new Error(response.error);
          }

          const { access, user } = response.data || {};

          // Guardar token en localStorage para las siguientes requests
          if (access) {
            localStorage.setItem("token", access);
          }

          set({
            token: access,
            user: user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      // Acción de logout
      logout: () => {
        // Limpiar token del localStorage
        localStorage.removeItem("token");

        set({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
        });
      },

      // Establecer usuario
      setUser: (user: User) => {
        set({ user });
      },

      // Establecer loading
      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },
    }),
    {
      name: "packfy-auth",
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
