import axios from 'axios';

// Función para determinar la URL base correcta
const getApiBaseURL = () => {
  const hostname = window.location.hostname;
  const port = window.location.port;
  
  console.log('🌐 API: Detectado hostname:', hostname, 'puerto:', port);
  
  // SIEMPRE usar el proxy cuando estamos en desarrollo con Vite
  if (port === '5173' || port === '5174' || port === '5175' || port === '5176') {
    console.log('📡 API: Usando proxy de Vite para todas las requests');
    return ''; // URL vacía = usar proxy relativo
  }
  
  // Si hay una variable de entorno específica para producción
  if (import.meta.env.VITE_API_BASE_URL) {
    console.log('🔧 API: Usando variable de entorno:', import.meta.env.VITE_API_BASE_URL);
    return import.meta.env.VITE_API_BASE_URL;
  }
  
  // Fallback directo al backend
  return 'http://localhost:8000';
};

// Crear instancia de axios con la URL base
export const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Log para debugging
console.log('API: Inicializando con baseURL:', api.defaults.baseURL);

// Interceptor para manejar tokens
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Interfaces
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

// API Auth
export const authAPI = {
  login: (email: string, password: string) =>
    api.post<LoginResponse>('/api/auth/login/', { email, password }),
  
  logout: () => 
    api.post('/api/auth/logout/'),
  
  getUser: () => 
    api.get<User>('/api/auth/user/'),
  
  register: (userData: Partial<User> & { password: string }) =>
    api.post<User>('/api/auth/register/', userData),
};

// API Empresas
export const empresasAPI = {
  getAll: (page: number = 1, pageSize: number = 10) =>
    api.get<{ results: Empresa[], count: number }>(`/api/empresas/?page=${page}&page_size=${pageSize}`),
  
  getById: (id: number) =>
    api.get<Empresa>(`/api/empresas/${id}/`),
  
  create: (empresa: Omit<Empresa, 'id'>) =>
    api.post<Empresa>('/api/empresas/', empresa),
  
  update: (id: number, empresa: Partial<Empresa>) =>
    api.put<Empresa>(`/api/empresas/${id}/`, empresa),
  
  delete: (id: number) =>
    api.delete(`/api/empresas/${id}/`),
};

// API Envios
export const enviosAPI = {
  getAll: (page: number = 1, pageSize: number = 10) =>
    api.get<{ results: Envio[], count: number }>(`/api/envios/?page=${page}&page_size=${pageSize}`),
  
  getById: (id: number) =>
    api.get<Envio>(`/api/envios/${id}/`),
  
  getByGuia: (numeroGuia: string) =>
    api.get<Envio>(`/api/envios/buscar_por_guia/?numero_guia=${numeroGuia}`),
  
  create: (envio: Omit<Envio, 'id' | 'numero_guia' | 'fecha_creacion' | 'fecha_actualizacion'>) =>
    api.post<Envio>('/api/envios/', envio),
  
  update: (id: number, envio: Partial<Envio>) =>
    api.put<Envio>(`/api/envios/${id}/`, envio),
  
  updateEstado: (id: number, estado: string) =>
    api.patch<Envio>(`/api/envios/${id}/`, { estado }),
  
  delete: (id: number) =>
    api.delete(`/api/envios/${id}/`),
  
  getEstadisticas: () =>
    api.get('/api/envios/estadisticas/'),
};

// API Público (sin autenticación)
export const publicAPI = {
  trackPackage: (numeroGuia: string) =>
    api.get<Envio>(`/api/public/track/${numeroGuia}/`),
};

export default api;
