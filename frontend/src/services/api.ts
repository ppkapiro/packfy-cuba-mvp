import axios from 'axios';

// Función para determinar la URL base correcta
const getApiBaseURL = () => {
  // Detectar si estamos en desarrollo y desde qué host
  const hostname = window.location.hostname;
  console.log('🌐 API: Detectado hostname:', hostname);
  
  // SIEMPRE usar el proxy cuando estamos en desarrollo
  // Esto funciona tanto para localhost como para IP
  if (window.location.port === '5173') {
    console.log('📡 API: Usando proxy de Vite para todas las requests');
    return ''; // URL vacía = usar proxy relativo
  }
  
  // Si hay una variable de entorno específica para producción
  if (import.meta.env.VITE_API_BASE_URL) {
    console.log('🔧 API: Usando variable de entorno:', import.meta.env.VITE_API_BASE_URL);
    return import.meta.env.VITE_API_BASE_URL;
  }
  
  // Si accedemos desde una IP (móvil), usar esa misma IP para el backend
  if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
    const apiUrl = `http://${hostname}:8000`;
    console.log('📱 API: Acceso desde móvil/IP detectado, usando:', apiUrl);
    return apiUrl;
  }
  
  // En localhost, usar localhost
  return 'http://localhost:8000';
};

// Crear instancia de axios con la URL base
export const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 15000, // Aumentado a 15 segundos para mayor tolerancia
  headers: {
    'Content-Type': 'application/json'
  }
});

// Log para debugging
console.log('API: Inicializando con baseURL:', api.defaults.baseURL);

// Determinar si estamos usando el tenant "ejemplo"
const useEjemploTenant = false;

// Instancia para peticiones públicas (sin token)
export const publicApi = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 15000, // Aumentado a 15 segundos
  headers: {
    'Content-Type': 'application/json'
  }
});

// Configurar los headers de autenticación si existe un token
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// Interceptor para manejar la renovación de tokens y otros errores
api.interceptors.response.use(
  (response: any) => {
    // Log para debugging
    if (response.config.url.includes('/auth/')) {
      console.log('API: Respuesta autenticación exitosa:', {
        url: response.config.url,
        status: response.status,
        hasToken: !!response.data.access
      });
    }
    return response;
  },
  async (error: any) => {
    const originalRequest = error.config;
    
    // Si no hay objeto de respuesta, estamos ante un error de red, probablemente
    if (!error.response) {
      console.error('API: Error de red detectado (posiblemente API no disponible):', error.message);
      // No redireccionar automáticamente, solo reportar el error para que la UI pueda manejarlo
      return Promise.reject({
        ...error,
        isNetworkError: true,
        friendlyMessage: 'No se pudo conectar con el servidor. Por favor, verifique su conexión a internet.'
      });
    }
    
    // Si el error es 401 (no autorizado) y no hemos intentado renovar el token
    if (error.response?.status === 401 && !originalRequest._retry) {
      console.log('API: Error 401 detectado, intentando renovar token');
      originalRequest._retry = true;
      
      try {
        // Intentar renovar el token
        const refreshToken = localStorage.getItem('refreshToken');
        
        if (!refreshToken) {
          // No hay refresh token, pero no hagamos redirección forzada
          console.log('API: No hay refresh token disponible');
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          sessionStorage.removeItem('_auth_success');
          // Dejar que el componente se encargue de la redirección
          return Promise.reject({
            ...error,
            isAuthError: true,
            authErrorType: 'no-refresh-token'
          });
        }
        
        // Llamar al endpoint de refresh, usando la ruta específica del tenant si es necesario
        const refreshEndpoint = useEjemploTenant 
          ? '/api/auth/ejemplo/refresh/' 
          : '/api/auth/refresh/';
            
        const response = await axios.post(
          `${api.defaults.baseURL}${refreshEndpoint}`,
          { refresh: refreshToken },
          // Configuración para evitar bucles infinitos en caso de error
          { _forceRefresh: true }
        );
        
        const { access } = response.data;
        
        console.log('API: Token renovado exitosamente');
        
        // Guardar el nuevo token
        localStorage.setItem('token', access);
        
        // Actualizar el header de autorización
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        originalRequest.headers['Authorization'] = `Bearer ${access}`;
        
        // Reintentar la petición original
        return api(originalRequest);
      } catch (refreshError) {        
        // Error al renovar el token, pero no forzar redirección
        console.error('API: Error al renovar el token:', refreshError);
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        sessionStorage.removeItem('_auth_success');
        
        // Dejar que el componente se encargue de la redirección
        return Promise.reject({
          ...error,
          isAuthError: true,
          authErrorType: 'refresh-failed',
          refreshError
        });
      }
    }
    
    return Promise.reject(error);
  }
);

// Función auxiliar para obtener la ruta correcta según el tenant
const getPath = (standardPath: string, ejemploPath: string) => {
  return useEjemploTenant ? ejemploPath : standardPath;
};

// API de Envíos
export const enviosAPI = {
  // Obtener todos los envíos con filtros opcionales y paginación
  getAll: (page = 1, pageSize = 10, filters = {}) => 
    api.get(getPath('/api/envios/', '/api/ejemplo/envios/'), { 
      params: { 
        page, 
        page_size: pageSize,
        ...filters 
      }
    }),
  
  // Obtener un envío por ID
  getById: (id: string) => api.get(getPath(`/api/envios/${id}/`, `/api/ejemplo/envios/${id}/`)),
  
  // Crear un nuevo envío
  create: (data: any) => api.post(getPath('/api/envios/', '/api/ejemplo/envios/'), data),
  
  // Actualizar un envío
  update: (id: string, data: any) => api.put(getPath(`/api/envios/${id}/`, `/api/ejemplo/envios/${id}/`), data),
  
  // Cambiar el estado de un envío
  changeStatus: (id: string, estado: string, comentario?: string, ubicacion?: string) => 
    api.post(getPath(`/api/envios/${id}/cambiar_estado/`, `/api/ejemplo/envios/${id}/cambiar_estado/`), 
      { estado, comentario, ubicacion }),
    
  // Obtener el historial de estados de un envío
  getHistory: (id: string) => api.get(getPath('/api/historial-estados/', '/api/ejemplo/historial-estados/'), 
    { params: { envio: id } }),
  
  // Buscar un envío por número de guía
  buscarPorGuia: (numeroGuia: string) => api.get(getPath('/api/envios/buscar_por_guia/', '/api/ejemplo/envios/buscar_por_guia/'), 
    { params: { numero_guia: numeroGuia } }),
  
  // Rastrear un envío públicamente por número de guía (sin autenticación)
  rastrearPublico: (numeroGuia: string) => publicApi.get('/api/envios/rastrear/', 
    { params: { numero_guia: numeroGuia } }),
};

// API de Autenticación
export const authAPI = {
  login: (email: string, password: string) => 
    api.post(getPath('/api/auth/login/', '/api/auth/ejemplo/login/'), { email, password }),
    
  refresh: (refreshToken: string) => 
    api.post(getPath('/api/auth/refresh/', '/api/auth/ejemplo/refresh/'), { refresh: refreshToken }),
    
  getCurrentUser: () => api.get(getPath('/api/usuarios/me/', '/api/ejemplo/usuarios/me/')),
};

// API de Usuarios
export const usuariosAPI = {
  getAll: () => api.get(getPath('/api/usuarios/', '/api/ejemplo/usuarios/')),
  
  getById: (id: string) => api.get(getPath(`/api/usuarios/${id}/`, `/api/ejemplo/usuarios/${id}/`)),
  
  create: (data: any) => api.post(getPath('/api/usuarios/', '/api/ejemplo/usuarios/'), data),
  
  update: (id: string, data: any) => api.put(getPath(`/api/usuarios/${id}/`, `/api/ejemplo/usuarios/${id}/`), data),
  
  changePassword: (id: string, oldPassword: string, newPassword: string) => 
    api.post(getPath(`/api/usuarios/${id}/change-password/`, `/api/ejemplo/usuarios/${id}/change-password/`), {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPassword
    }),
};
