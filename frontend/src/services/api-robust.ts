// 🎯 PACKFY CUBA - API ROBUSTA Y AUTOCONFIGURADA
// Sistema que se adapta automáticamente sin problemas de proxy

import axios, { AxiosInstance } from 'axios';
import { apiManager } from './api-manager';

// Crear instancia de axios con configuración automática
const createApiInstance = (): AxiosInstance => {
  const config = apiManager.getConfig();
  
  const instance = axios.create({
    baseURL: apiManager.getBaseURL(),
    timeout: 15000,
    headers: {
      'Content-Type': 'application/json'
    },
    withCredentials: true
  });

  console.log(`🚀 API configurada: ${config.mode} mode, baseURL: ${instance.defaults.baseURL}`);

  // Interceptor para agregar token
  instance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Interceptor para manejar errores y auto-reparación
  instance.interceptors.response.use(
    (response) => response,
    async (error) => {
      // Si hay error de conexión, intentar auto-reparación
      if (!error.response && error.code === 'NETWORK_ERROR') {
        console.log('🔧 Error de red detectado, intentando auto-reparación...');
        
        const fixed = await apiManager.autoFix();
        if (fixed) {
          // Recrear la instancia con nueva configuración
          instance.defaults.baseURL = apiManager.getBaseURL();
          console.log('✅ API reparada, reintentando request...');
          
          // Reintentar el request original
          return instance.request(error.config);
        }
      }

      // Manejar token expirado
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }
      }

      return Promise.reject(error);
    }
  );

  return instance;
};

// Instancia principal
export const api = createApiInstance();

// Función para recrear la API si es necesario
export const refreshApi = () => {
  const newInstance = createApiInstance();
  Object.setPrototypeOf(api, Object.getPrototypeOf(newInstance));
  Object.assign(api, newInstance);
};

// Interfaces de tipos
export interface User {
  id: number;
  email: string;
  nombre: string;
  apellidos: string;
  tipo_usuario: 'empresa' | 'cliente' | 'admin';
  telefono?: string;
  direccion?: string;
  is_active: boolean;
  date_joined: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface Empresa {
  id: number;
  nombre: string;
  direccion: string;
  telefono: string;
  email: string;
  is_active: boolean;
}

export interface Envio {
  id: number;
  numero_guia: string;
  remitente_nombre: string;
  remitente_telefono: string;
  remitente_direccion: string;
  destinatario_nombre: string;
  destinatario_telefono: string;
  destinatario_direccion: string;
  descripcion_contenido: string;
  peso: number;
  valor_declarado: number;
  costo_envio: number;
  estado: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
  empresa: number;
  usuario_creador: number;
}

// Función helper para construir URLs
const buildUrl = (endpoint: string): string => {
  const config = apiManager.getConfig();
  if (config.mode === 'proxy') {
    return endpoint.startsWith('/api') ? endpoint : `/api${endpoint}`;
  }
  return endpoint.startsWith('/api') ? endpoint : `/api${endpoint}`;
};

// APIs específicas con auto-reparación integrada
export const authAPI = {
  login: async (email: string, password: string) => {
    try {
      return await api.post<LoginResponse>(buildUrl('/auth/login/'), { email, password });
    } catch (error) {
      console.log('🔧 Error en login, verificando conexión...');
      await apiManager.autoFix();
      refreshApi();
      return api.post<LoginResponse>(buildUrl('/auth/login/'), { email, password });
    }
  },
  
  logout: () => api.post(buildUrl('/auth/logout/')),
  
  getUser: async () => {
    try {
      return await api.get<User>(buildUrl('/auth/user/'));
    } catch (error) {
      await apiManager.autoFix();
      refreshApi();
      return api.get<User>(buildUrl('/auth/user/'));
    }
  },
  
  register: (userData: Partial<User> & { password: string }) =>
    api.post<User>(buildUrl('/auth/register/'), userData),
};

export const empresasAPI = {
  getAll: (page: number = 1, pageSize: number = 10) =>
    api.get<{ results: Empresa[], count: number }>(buildUrl(`/empresas/?page=${page}&page_size=${pageSize}`)),
  
  getById: (id: number) =>
    api.get<Empresa>(buildUrl(`/empresas/${id}/`)),
  
  create: (empresa: Omit<Empresa, 'id'>) =>
    api.post<Empresa>(buildUrl('/empresas/'), empresa),
  
  update: (id: number, empresa: Partial<Empresa>) =>
    api.put<Empresa>(buildUrl(`/empresas/${id}/`), empresa),
  
  delete: (id: number) =>
    api.delete(buildUrl(`/empresas/${id}/`)),
};

export const enviosAPI = {
  getAll: async (page: number = 1, pageSize: number = 10) => {
    try {
      return await api.get<{ results: Envio[], count: number }>(buildUrl(`/envios/?page=${page}&page_size=${pageSize}`));
    } catch (error) {
      await apiManager.autoFix();
      refreshApi();
      return api.get<{ results: Envio[], count: number }>(buildUrl(`/envios/?page=${page}&page_size=${pageSize}`));
    }
  },
  
  getById: (id: number) =>
    api.get<Envio>(buildUrl(`/envios/${id}/`)),
  
  getByGuia: (numeroGuia: string) =>
    api.get<Envio>(buildUrl(`/envios/buscar_por_guia/?numero_guia=${numeroGuia}`)),
  
  create: (envio: Omit<Envio, 'id' | 'numero_guia' | 'fecha_creacion' | 'fecha_actualizacion'>) =>
    api.post<Envio>(buildUrl('/envios/'), envio),
  
  update: (id: number, envio: Partial<Envio>) =>
    api.put<Envio>(buildUrl(`/envios/${id}/`), envio),
  
  updateEstado: (id: number, estado: string) =>
    api.patch<Envio>(buildUrl(`/envios/${id}/`), { estado }),
  
  delete: (id: number) =>
    api.delete(buildUrl(`/envios/${id}/`)),
  
  getEstadisticas: () =>
    api.get(buildUrl('/envios/estadisticas/')),
};

export const publicAPI = {
  trackPackage: (numeroGuia: string) =>
    api.get<Envio>(buildUrl(`/public/track/${numeroGuia}/`)),
};

// Test de conectividad público
export const testConnection = async (): Promise<boolean> => {
  return await apiManager.testConnection();
};

// Información de configuración para debugging
export const getApiInfo = () => {
  return {
    config: apiManager.getConfig(),
    baseURL: api.defaults.baseURL,
    manager: apiManager
  };
};

export default api;
