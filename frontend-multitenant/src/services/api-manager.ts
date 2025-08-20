// 🎯 PACKFY CUBA - CONFIGURACIÓN AUTOMÁTICA DE API
// Sistema autodetectado que elimina problemas de proxy permanentemente

interface ApiConfig {
  baseURL: string;
  mode: 'proxy' | 'direct';
  detected: {
    hostname: string;
    port: string;
    environment: 'development' | 'production';
    platform: 'desktop' | 'mobile';
  };
}

class PackfyApiManager {
  private config: ApiConfig;
  private backendPorts = [8000, 8001, 8080, 3001];
  private frontendPorts = [5173, 5174, 5175, 5176, 5177, 3000];

  constructor() {
    this.config = this.detectConfiguration();
    console.log('🎯 Packfy API Manager inicializado:', this.config);
  }

  private detectConfiguration(): ApiConfig {
    const hostname = window.location.hostname;
    const port = window.location.port;
    const protocol = window.location.protocol;

    // Detectar entorno
    const isDevelopment = hostname === 'localhost' || hostname === '127.0.0.1' || hostname.startsWith('192.168.');
    const isMobile = hostname.startsWith('192.168.') && hostname !== 'localhost';

    console.log('🔍 Detectando configuración:', { hostname, port, protocol, isDevelopment, isMobile });

    // Configuración base
    const config: ApiConfig = {
      baseURL: '',
      mode: 'direct',
      detected: {
        hostname,
        port,
        environment: isDevelopment ? 'development' : 'production',
        platform: isMobile ? 'mobile' : 'desktop'
      }
    };

    // ESTRATEGIA 1: Desarrollo con puertos conocidos de Vite
    if (isDevelopment && this.frontendPorts.includes(parseInt(port))) {
      // En desarrollo, intentar proxy primero
      config.baseURL = '';
      config.mode = 'proxy';
      console.log('✅ Modo: Proxy de desarrollo');
      return config;
    }

    // ESTRATEGIA 2: Conexión directa para móvil
    if (isMobile) {
      config.baseURL = `http://${hostname}:8000`;
      config.mode = 'direct';
      console.log('✅ Modo: Directo móvil');
      return config;
    }

    // ESTRATEGIA 3: Desarrollo con conexión directa
    if (isDevelopment) {
      config.baseURL = 'http://localhost:8000';
      config.mode = 'direct';
      console.log('✅ Modo: Directo local');
      return config;
    }

    // ESTRATEGIA 4: Producción
    config.baseURL = import.meta.env.VITE_API_BASE_URL || '/api';
    config.mode = 'direct';
    console.log('✅ Modo: Producción');
    return config;
  }

  public getBaseURL(): string {
    return this.config.baseURL;
  }

  public getConfig(): ApiConfig {
    return { ...this.config };
  }

  public async testConnection(): Promise<boolean> {
    try {
      const testUrl = this.config.mode === 'proxy' 
        ? '/api/auth/user/' 
        : `${this.config.baseURL}/api/auth/user/`;
      
      const response = await fetch(testUrl, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
      });

      const isWorking = response.status === 200 || response.status === 401;
      console.log(`🔍 Test de conexión: ${isWorking ? 'SUCCESS' : 'FAILED'}`);
      return isWorking;
    } catch (error) {
      console.log('🔍 Test de conexión: FAILED', error);
      return false;
    }
  }

  public async autoFix(): Promise<boolean> {
    console.log('🔧 Iniciando auto-reparación...');
    
    // Si el proxy falla, cambiar a directo
    if (this.config.mode === 'proxy' && !(await this.testConnection())) {
      console.log('🔄 Proxy falló, cambiando a modo directo...');
      
      if (this.config.detected.platform === 'mobile') {
        this.config.baseURL = `http://${this.config.detected.hostname}:8000`;
      } else {
        this.config.baseURL = 'http://localhost:8000';
      }
      
      this.config.mode = 'direct';
      
      if (await this.testConnection()) {
        console.log('✅ Auto-reparación exitosa!');
        return true;
      }
    }

    // Probar diferentes puertos del backend
    for (const port of this.backendPorts) {
      const testURL = this.config.detected.platform === 'mobile' 
        ? `http://${this.config.detected.hostname}:${port}`
        : `http://localhost:${port}`;
      
      this.config.baseURL = testURL;
      this.config.mode = 'direct';
      
      if (await this.testConnection()) {
        console.log(`✅ Backend encontrado en puerto ${port}`);
        return true;
      }
    }

    console.log('❌ Auto-reparación falló');
    return false;
  }
}

// Instancia global
export const apiManager = new PackfyApiManager();

export default apiManager;
