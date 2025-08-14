// 🇨🇺 PACKFY CUBA - Cliente API Seguro v4.0
// Sistema de autenticación y comunicación con el backend

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import toast from "react-hot-toast";

interface AuthTokens {
  access: string;
  refresh: string;
  access_expires: number;
  refresh_expires: number;
}

interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
  detail?: string;
  status: number;
}

interface UserProfile {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  empresa: any;
  es_administrador_empresa: boolean;
}

class SecureApiClient {
  private static instance: SecureApiClient;
  private client: AxiosInstance;
  private tokens: AuthTokens | null = null;
  private refreshPromise: Promise<string> | null = null;
  private baseURL: string;

  private constructor() {
    this.baseURL = this.determineBaseURL();
    this.client = this.createAxiosInstance();
    this.loadTokensFromStorage();
    this.setupInterceptors();
  }

  static getInstance(): SecureApiClient {
    if (!SecureApiClient.instance) {
      SecureApiClient.instance = new SecureApiClient();
    }
    return SecureApiClient.instance;
  }

  private determineBaseURL(): string {
    const hostname = window.location.hostname;
    const isDev = hostname === "localhost" || hostname === "127.0.0.1";

    if (isDev) {
      return `${window.location.protocol}//${hostname}:8000`;
    } else {
      return `${window.location.protocol}//api.${hostname}`;
    }
  }

  private createAxiosInstance(): AxiosInstance {
    return axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest", // CSRF protection
      },
    });
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token
        if (this.tokens?.access) {
          config.headers.Authorization = `Bearer ${this.tokens.access}`;
        }

        // Add timestamp for cache busting
        if (config.method === "get") {
          config.params = { ...config.params, _t: Date.now() };
        }

        console.log(
          `🔹 API Request: ${config.method?.toUpperCase()} ${config.url}`
        );
        return config;
      },
      (error) => {
        console.error("🔴 Request error:", error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(
          `🔸 API Response: ${response.status} ${response.config.url}`
        );
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        // Handle 401 errors with token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newAccessToken = await this.refreshAccessToken();
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            this.logout();
            window.location.href = "/login";
            return Promise.reject(refreshError);
          }
        }

        // Handle other errors
        this.handleApiError(error);
        return Promise.reject(error);
      }
    );
  }

  private handleApiError(error: any): void {
    const status = error.response?.status;
    const message =
      error.response?.data?.detail ||
      error.response?.data?.error ||
      error.message;

    console.error(`🔴 API Error ${status}:`, message);

    // Show user-friendly error messages
    switch (status) {
      case 400:
        toast.error("Solicitud inválida: " + message);
        break;
      case 401:
        toast.error("Sesión expirada. Por favor, inicia sesión nuevamente.");
        break;
      case 403:
        toast.error("No tienes permisos para realizar esta acción.");
        break;
      case 404:
        toast.error("Recurso no encontrado.");
        break;
      case 429:
        toast.error("Demasiadas solicitudes. Intenta más tarde.");
        break;
      case 500:
        toast.error("Error del servidor. Intenta más tarde.");
        break;
      default:
        if (message.includes("Network Error")) {
          toast.error("Error de conexión. Verifica tu internet.");
        } else {
          toast.error("Ha ocurrido un error inesperado.");
        }
    }
  }

  // Auth methods
  async login(username: string, password: string): Promise<UserProfile> {
    try {
      const response = await this.client.post("/api/auth/login/", {
        username,
        password,
      });

      const tokens: AuthTokens = {
        access: response.data.access,
        refresh: response.data.refresh,
        access_expires: response.data.access_expires,
        refresh_expires: response.data.refresh_expires,
      };

      this.setTokens(tokens);

      // Get user profile
      const profileResponse = await this.client.get("/api/auth/profile/");
      const userProfile = profileResponse.data.user;

      toast.success(`¡Bienvenido, ${userProfile.first_name}!`);
      return userProfile;
    } catch (error: any) {
      console.error("🔴 Login error:", error);

      if (error.response?.status === 401) {
        throw new Error("Credenciales incorrectas");
      } else if (error.response?.status === 403) {
        throw new Error("Cuenta bloqueada temporalmente");
      } else {
        throw new Error("Error de conexión");
      }
    }
  }

  async logout(): Promise<void> {
    try {
      if (this.tokens?.refresh) {
        await this.client.post("/api/auth/logout/", {
          refresh_token: this.tokens.refresh,
        });
      }
    } catch (error) {
      console.error("🔴 Logout error:", error);
    } finally {
      this.clearTokens();
      toast.success("Sesión cerrada correctamente");
    }
  }

  async refreshAccessToken(): Promise<string> {
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    if (!this.tokens?.refresh) {
      throw new Error("No refresh token available");
    }

    this.refreshPromise = new Promise(async (resolve, reject) => {
      try {
        const response = await axios.post(`${this.baseURL}/api/auth/refresh/`, {
          refresh: this.tokens!.refresh,
        });

        const newAccessToken = response.data.access;
        this.tokens!.access = newAccessToken;
        this.tokens!.access_expires = response.data.access_expires;

        this.saveTokensToStorage();

        console.log("🔄 Token refreshed successfully");
        resolve(newAccessToken);
      } catch (error) {
        console.error("🔴 Token refresh failed:", error);
        reject(error);
      } finally {
        this.refreshPromise = null;
      }
    });

    return this.refreshPromise;
  }

  async getUserProfile(): Promise<UserProfile> {
    const response = await this.client.get("/api/auth/profile/");
    return response.data.user;
  }

  async changePassword(
    oldPassword: string,
    newPassword: string
  ): Promise<void> {
    await this.client.post("/api/auth/change-password/", {
      old_password: oldPassword,
      new_password: newPassword,
    });
    toast.success("Contraseña cambiada exitosamente");
  }

  // Token management
  private setTokens(tokens: AuthTokens): void {
    this.tokens = tokens;
    this.saveTokensToStorage();
  }

  private saveTokensToStorage(): void {
    if (this.tokens) {
      localStorage.setItem("packfy_tokens", JSON.stringify(this.tokens));
    }
  }

  private loadTokensFromStorage(): void {
    try {
      const storedTokens = localStorage.getItem("packfy_tokens");
      if (storedTokens) {
        this.tokens = JSON.parse(storedTokens);

        // Check if tokens are expired
        const now = Date.now() / 1000;
        if (this.tokens && this.tokens.refresh_expires < now) {
          this.clearTokens();
        }
      }
    } catch (error) {
      console.error("🔴 Error loading tokens:", error);
      this.clearTokens();
    }
  }

  private clearTokens(): void {
    this.tokens = null;
    localStorage.removeItem("packfy_tokens");
    localStorage.removeItem("token"); // Legacy support
  }

  // Utility methods
  isAuthenticated(): boolean {
    return !!this.tokens?.access;
  }

  getAccessToken(): string | null {
    return this.tokens?.access || null;
  }

  // Generic API methods
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get(url, config);
    return response.data;
  }

  async post<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.put(url, data, config);
    return response.data;
  }

  async patch<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.patch(url, data, config);
    return response.data;
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete(url, config);
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      await this.client.get("/api/sistema-info/");
      return true;
    } catch (error) {
      console.error("🔴 Health check failed:", error);
      return false;
    }
  }
}

// Export singleton instance
export const api = SecureApiClient.getInstance();
export default api;

// Export types
export type { AuthTokens, ApiResponse, UserProfile };
