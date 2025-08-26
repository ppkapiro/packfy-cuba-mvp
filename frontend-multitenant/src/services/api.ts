// 🇨🇺 PACKFY CUBA - API UNIFICADA Y ROBUSTA v3.0
// Sistema único de configuración de API para todas las conexiones

import { initializeTenantFromHostname } from "../utils/tenantDetector";

interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

class PackfyApiClient {
  private static instance: PackfyApiClient;
  private baseURL: string = "";
  private isConfigured: boolean = false;
  private tenantSlug: string | null = null;

  private constructor() {
    this.configure();
  }

  static getInstance(): PackfyApiClient {
    if (!PackfyApiClient.instance) {
      PackfyApiClient.instance = new PackfyApiClient();
    }
    return PackfyApiClient.instance;
  }

  private configure(): void {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    const port = window.location.port;

    console.log("🇨🇺 Packfy API configurándose...", {
      hostname,
      protocol,
      port,
    });

    // Estrategia de configuración inteligente
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      // Desarrollo local - usar proxy para evitar problemas de CORS
      this.baseURL = port === "5173" ? "/api" : "http://localhost:8000/api";
    } else if (
      hostname.match(/^192\.168\.|^10\.|^172\.(1[6-9]|2[0-9]|3[0-1])\./)
    ) {
      // Red local (móvil/LAN) - usar proxy para evitar Mixed Content
      this.baseURL = "/api";
    } else {
      // Producción o dominio externo
      this.baseURL = `${protocol}//${hostname}/api`;
    }

    // Inicializar tenant automáticamente desde hostname
    const autoTenantSlug = initializeTenantFromHostname();
    if (autoTenantSlug && !this.tenantSlug) {
      this.setTenantSlug(autoTenantSlug);
    }

    this.isConfigured = true;
    console.log("✅ Packfy API configurada:", this.baseURL);
    console.log("🏢 Tenant configurado:", this.tenantSlug);
  }

  getBaseURL(): string {
    if (!this.isConfigured) {
      this.configure();
    }
    return this.baseURL;
  }

  // Configuración multi-tenant
  setTenantSlug(slug: string): void {
    this.tenantSlug = slug;
    console.log(`🏢 Tenant configurado: ${slug}`);
  }

  clearTenantSlug(): void {
    this.tenantSlug = null;
    console.log("🏢 Tenant limpiado");
  }

  getTenantSlug(): string | null {
    return this.tenantSlug;
  }

  async makeRequest<T>(
    endpoint: string,
    method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE" = "GET",
    data?: any,
    headers?: Record<string, string>
  ): Promise<ApiResponse<T>> {
    try {
      const token = localStorage.getItem("token");

      const config: RequestInit = {
        method,
        headers: {
          "Content-Type": "application/json",
          ...(token && { Authorization: `Bearer ${token}` }),
          ...(this.tenantSlug && { "X-Tenant-Slug": this.tenantSlug }),
          ...headers,
        },
      };

      if (data && method !== "GET") {
        config.body = JSON.stringify(data);
      }

      const url = `${this.getBaseURL()}${endpoint}`;
      console.log(`📡 API Request: ${method} ${url}`);

      const response = await fetch(url, config);

      let responseData;
      try {
        responseData = await response.json();
      } catch {
        responseData = null;
      }

      const result: ApiResponse<T> = {
        data: responseData,
        status: response.status,
      };

      if (!response.ok) {
        result.error =
          responseData?.detail ||
          responseData?.message ||
          `HTTP ${response.status}`;
        console.error("❌ API Error:", result.error);
      } else {
        console.log("✅ API Success:", method, endpoint);
      }

      return result;
    } catch (error) {
      console.error("🚨 API Request Failed:", error);
      return {
        status: 0,
        error: error instanceof Error ? error.message : "Network Error",
      };
    }
  }

  // Métodos de autenticación
  async login(email: string, password: string) {
    return this.makeRequest("/auth/login/", "POST", { email, password });
  }

  async logout() {
    return this.makeRequest("/auth/logout/", "POST");
  }

  async getCurrentUser() {
    return this.makeRequest("/usuarios/me/");
  }

  async register(userData: any) {
    return this.makeRequest("/auth/register/", "POST", userData);
  }

  // Métodos de empresas
  async getEmpresas(page = 1, pageSize = 10) {
    return this.makeRequest(`/empresas/?page=${page}&page_size=${pageSize}`);
  }

  async getEmpresa(id: number) {
    return this.makeRequest(`/empresas/${id}/`);
  }

  async createEmpresa(empresa: any) {
    return this.makeRequest("/empresas/", "POST", empresa);
  }

  async updateEmpresa(id: number, empresa: any) {
    return this.makeRequest(`/empresas/${id}/`, "PUT", empresa);
  }

  async deleteEmpresa(id: number) {
    return this.makeRequest(`/empresas/${id}/`, "DELETE");
  }

  // Métodos de envíos
  async getEnvios(page = 1, pageSize = 10, filters?: any) {
    let url = `/envios/?page=${page}&page_size=${pageSize}`;
    if (filters) {
      const queryParams = new URLSearchParams(filters).toString();
      url += `&${queryParams}`;
    }
    return this.makeRequest(url);
  }

  async getEnvio(id: number) {
    return this.makeRequest(`/envios/${id}/`);
  }

  async getEnvioByGuia(numeroGuia: string) {
    return this.makeRequest(`/envios/rastrear/?numero_guia=${numeroGuia}`);
  }

  async createEnvio(envio: any) {
    return this.makeRequest("/envios/", "POST", envio);
  }

  async updateEnvio(id: number, envio: any) {
    return this.makeRequest(`/envios/${id}/`, "PUT", envio);
  }

  async updateEnvioEstado(id: number, estado: string) {
    return this.makeRequest(`/envios/${id}/`, "PATCH", { estado });
  }

  async deleteEnvio(id: number) {
    return this.makeRequest(`/envios/${id}/`, "DELETE");
  }

  async getEstadisticas() {
    return this.makeRequest("/envios/estadisticas/");
  }

  // Métodos públicos
  async trackPublic(numeroGuia: string) {
    return this.makeRequest(`/envios/rastrear/?numero_guia=${numeroGuia}`);
  }

  // Test de conectividad
  async testConnection(): Promise<boolean> {
    try {
      const response = await this.makeRequest("/");
      return response.status === 200;
    } catch {
      return false;
    }
  }

  // Información de configuración
  getConfig() {
    return {
      baseURL: this.getBaseURL(),
      configured: this.isConfigured,
      timestamp: new Date().toISOString(),
    };
  }
}

// Instancia singleton
const apiClient = PackfyApiClient.getInstance();

// Exportaciones para compatibilidad
export const api = {
  get: (url: string) => apiClient.makeRequest(url, "GET"),
  post: (url: string, data?: any) => apiClient.makeRequest(url, "POST", data),
  put: (url: string, data?: any) => apiClient.makeRequest(url, "PUT", data),
  patch: (url: string, data?: any) => apiClient.makeRequest(url, "PATCH", data),
  delete: (url: string) => apiClient.makeRequest(url, "DELETE"),
};

export const authAPI = {
  login: (email: string, password: string) => apiClient.login(email, password),
  logout: () => apiClient.logout(),
  getCurrentUser: () => apiClient.getCurrentUser(),
  refresh: (refreshToken: string) =>
    apiClient.makeRequest("/auth/refresh/", "POST", { refresh: refreshToken }),
  register: (userData: any) => apiClient.register(userData),
};

export const empresasAPI = {
  getAll: (page = 1, pageSize = 10) => apiClient.getEmpresas(page, pageSize),
  getById: (id: number) => apiClient.getEmpresa(id),
  create: (empresa: any) => apiClient.createEmpresa(empresa),
  update: (id: number, empresa: any) => apiClient.updateEmpresa(id, empresa),
  delete: (id: number) => apiClient.deleteEmpresa(id),
};

export const enviosAPI = {
  getAll: (page = 1, pageSize = 10, filters?: any) =>
    apiClient.getEnvios(page, pageSize, filters),
  getById: (id: number) => apiClient.getEnvio(id),
  getByGuia: (numeroGuia: string) => apiClient.getEnvioByGuia(numeroGuia),
  create: (envio: any) => apiClient.createEnvio(envio),
  update: (id: number, envio: any) => apiClient.updateEnvio(id, envio),
  updateEstado: (id: number, estado: string) =>
    apiClient.updateEnvioEstado(id, estado),
  delete: (id: number) => apiClient.deleteEnvio(id),
  getEstadisticas: () => apiClient.getEstadisticas(),
};

export const publicAPI = {
  trackPackage: (numeroGuia: string) => apiClient.trackPublic(numeroGuia),
  searchByRemitente: (nombre: string) =>
    apiClient.makeRequest(
      `/envios/buscar_por_remitente/?nombre=${encodeURIComponent(nombre)}`
    ),
  searchByDestinatario: (nombre: string) =>
    apiClient.makeRequest(
      `/envios/buscar_por_destinatario/?nombre=${encodeURIComponent(nombre)}`
    ),
};

// Funciones de utilidad
export const testConnection = () => apiClient.testConnection();
export const getApiInfo = () => apiClient.getConfig();

console.log("🇨🇺 Packfy API Unificada v3.0 cargada:", apiClient.getConfig());

export default apiClient;
