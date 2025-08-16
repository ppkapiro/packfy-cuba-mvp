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
        const resp = await authAPI.login(email, password);
        const ok = resp.status >= 200 && resp.status < 300 && !!resp.data;
        if (!ok) {
          set({ isLoading: false });
          throw new Error(resp.error || "Error de autenticación");
        }
        const d: any = resp.data;
        const access = d?.access as string | undefined;
        const user = d?.user as any;
        if (access) {
          try {
            localStorage.setItem("token", access);
          } catch {}
        }
        set({
          token: access || null,
          user: user || null,
          isAuthenticated: !!access,
          isLoading: false,
        });
      },

      // Acción de logout
      logout: () => {
        // Limpiar token local
        try {
          localStorage.removeItem("token");
          localStorage.removeItem("refreshToken");
        } catch {}
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
      onRehydrateStorage: () => () => {
        // Nada adicional: el cliente usa fetch y lee token desde store
      },
    }
  )
);
