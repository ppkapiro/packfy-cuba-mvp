// 🎯 PACKFY CUBA - SISTEMA AUTOCONFIGURADO DEFINITIVO
// Elimina problemas de proxy de forma permanente

class PackfyAutoConfig {
  private static instance: PackfyAutoConfig;
  private baseURL: string = '';
  private isConfigured: boolean = false;

  private constructor() {
    this.configure();
  }

  static getInstance(): PackfyAutoConfig {
    if (!PackfyAutoConfig.instance) {
      PackfyAutoConfig.instance = new PackfyAutoConfig();
    }
    return PackfyAutoConfig.instance;
  }

  private configure(): void {
    const hostname = window.location.hostname;
    const port = window.location.port;

    console.log('🎯 Packfy Auto-Config iniciando...', { hostname, port });

    // ESTRATEGIA SIMPLE: Conexión directa siempre
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      this.baseURL = 'http://localhost:8000';
    } else if (hostname.startsWith('192.168.')) {
      this.baseURL = `http://${hostname}:8000`;
    } else {
      // Producción o dominio personalizado
      this.baseURL = `${window.location.protocol}//${hostname}:8000`;
    }

    this.isConfigured = true;
    console.log('✅ Packfy configurado:', this.baseURL);
  }

  getBaseURL(): string {
    if (!this.isConfigured) {
      this.configure();
    }
    return this.baseURL;
  }

  async testBackend(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/admin/`, {
        method: 'HEAD',
        mode: 'no-cors'
      });
      return true;
    } catch {
      // Probar puerto alternativo
      const altURL = this.baseURL.replace(':8000', ':8001');
      try {
        await fetch(`${altURL}/admin/`, {
          method: 'HEAD', 
          mode: 'no-cors'
        });
        this.baseURL = altURL;
        console.log('✅ Backend encontrado en puerto alternativo:', altURL);
        return true;
      } catch {
        console.log('❌ Backend no disponible');
        return false;
      }
    }
  }
}

// Configurador global
export const autoConfig = PackfyAutoConfig.getInstance();

// API simplificada sin axios para evitar problemas
class PackfyAPI {
  private makeRequest = async (url: string, options: RequestInit = {}): Promise<Response> => {
    const fullURL = `${autoConfig.getBaseURL()}${url}`;
    
    const token = localStorage.getItem('token');
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers
    };

    try {
      const response = await fetch(fullURL, {
        ...options,
        headers,
        credentials: 'include'
      });

      // Auto logout en 401
      if (response.status === 401 && !url.includes('/login')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }

      return response;
    } catch (error) {
      console.log('🔧 Request failed, testing backend...');
      await autoConfig.testBackend();
      
      // Reintentar con nueva configuración
      const retryURL = `${autoConfig.getBaseURL()}${url}`;
      return fetch(retryURL, {
        ...options,
        headers,
        credentials: 'include'
      });
    }
  };

  // Métodos HTTP simplificados
  async get(url: string) {
    const response = await this.makeRequest(url, { method: 'GET' });
    return response.json();
  }

  async post(url: string, data: any) {
    const response = await this.makeRequest(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async put(url: string, data: any) {
    const response = await this.makeRequest(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async patch(url: string, data: any) {
    const response = await this.makeRequest(url, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async delete(url: string) {
    const response = await this.makeRequest(url, { method: 'DELETE' });
    return response.ok;
  }
}

// Instancia global de la API
const api = new PackfyAPI();

// APIs específicas con la nueva implementación
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/api/auth/login/', { email, password }),
  
  logout: () => 
    api.post('/api/auth/logout/', {}),
  
  getUser: () => 
    api.get('/api/auth/user/'),
  
  register: (userData: any) =>
    api.post('/api/auth/register/', userData),
};

export const empresasAPI = {
  getAll: (page: number = 1, pageSize: number = 10) =>
    api.get(`/api/empresas/?page=${page}&page_size=${pageSize}`),
  
  getById: (id: number) =>
    api.get(`/api/empresas/${id}/`),
  
  create: (empresa: any) =>
    api.post('/api/empresas/', empresa),
  
  update: (id: number, empresa: any) =>
    api.put(`/api/empresas/${id}/`, empresa),
  
  delete: (id: number) =>
    api.delete(`/api/empresas/${id}/`),
};

export const enviosAPI = {
  getAll: (page: number = 1, pageSize: number = 10) =>
    api.get(`/api/envios/?page=${page}&page_size=${pageSize}`),
  
  getById: (id: number) =>
    api.get(`/api/envios/${id}/`),
  
  getByGuia: (numeroGuia: string) =>
    api.get(`/api/envios/buscar_por_guia/?numero_guia=${numeroGuia}`),
  
  create: (envio: any) =>
    api.post('/api/envios/', envio),
  
  update: (id: number, envio: any) =>
    api.put(`/api/envios/${id}/`, envio),
  
  updateEstado: (id: number, estado: string) =>
    api.patch(`/api/envios/${id}/`, { estado }),
  
  delete: (id: number) =>
    api.delete(`/api/envios/${id}/`),
  
  getEstadisticas: () =>
    api.get('/api/envios/estadisticas/'),
};

export const publicAPI = {
  trackPackage: (numeroGuia: string) =>
    api.get(`/api/public/track/${numeroGuia}/`),
};

// Test de conectividad
export const testConnection = async (): Promise<boolean> => {
  return await autoConfig.testBackend();
};

// Obtener información de configuración
export const getApiInfo = () => ({
  baseURL: autoConfig.getBaseURL(),
  configured: true,
  strategy: 'direct-connection'
});

console.log('🚀 Packfy API autoconfigurada:', autoConfig.getBaseURL());

export default api;
