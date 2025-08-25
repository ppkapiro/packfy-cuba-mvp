import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiClient from '../services/api';

// Tipos para el sistema multi-tenant
interface Empresa {
  id: number;
  nombre: string;
  slug: string;
  activo: boolean;
  descripcion?: string;
  configuracion?: Record<string, any>;
  fecha_creacion: string;
}

interface PerfilUsuario {
  rol: 'dueno' | 'operador_miami' | 'operador_cuba' | 'remitente' | 'destinatario';
  fecha_ingreso: string;
  configuracion?: Record<string, any>;
}

interface TenantContextData {
  // Estado actual
  empresaActual: Empresa | null;
  perfilActual: PerfilUsuario | null;
  empresasDisponibles: Empresa[];
  isLoading: boolean;

  // Estado de dominios
  dominioActual: string;
  esSubdominio: boolean;
  esDominioAdmin: boolean;

  // Acciones
  cambiarEmpresa: (empresaSlug: string, empresaData?: Empresa) => Promise<void>;
  cargarEmpresas: () => Promise<void>;
  obtenerPerfilEnEmpresa: () => Promise<void>;

  // Navegación por dominios
  redirigirAEmpresa: (empresaSlug: string) => void;
  redirigirAAdmin: () => void;

  // Utilidades
  puedeEjecutarAccion: (accion: string) => boolean;
  esAdministrador: () => boolean;
}

// Contexto
const TenantContext = createContext<TenantContextData>({} as TenantContextData);

// Provider del contexto multi-tenant
export const TenantProvider = ({ children }: { children: ReactNode }) => {
  const [empresaActual, setEmpresaActual] = useState<Empresa | null>(null);
  const [perfilActual, setPerfilActual] = useState<PerfilUsuario | null>(null);
  const [empresasDisponibles, setEmpresasDisponibles] = useState<Empresa[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Estados de dominio
  const [dominioActual, setDominioActual] = useState<string>('');
  const [esSubdominio, setEsSubdominio] = useState<boolean>(false);
  const [esDominioAdmin, setEsDominioAdmin] = useState<boolean>(false);

  // FUNCIONES DE DETECCIÓN DE DOMINIOS
  const detectarDominio = () => {
    const hostname = window.location.hostname;
    const port = window.location.port;
    const fullHost = port ? `${hostname}:${port}` : hostname;

    console.log('🌐 TenantContext: Detectando dominio:', fullHost);

    setDominioActual(fullHost);

    // Detectar si es subdominio específico de empresa
    const empresaSlug = extraerEmpresaDeSubdominio(hostname);
    if (empresaSlug) {
      console.log('🏢 TenantContext: Subdominio de empresa detectado:', empresaSlug);
      setEsSubdominio(true);
      setEsDominioAdmin(false);
      return empresaSlug;
    }

    // Detectar si es dominio administrativo
    const esAdmin = esHostAdministrativo(hostname);
    console.log('👨‍💼 TenantContext: ¿Es dominio admin?', esAdmin);
    setEsSubdominio(false);
    setEsDominioAdmin(esAdmin);

    return null;
  };

  const extraerEmpresaDeSubdominio = (hostname: string): string | null => {
    // Patrones para detectar subdominios de empresa
    const patterns = [
      /^([^.]+)\.packfy\.com$/,    // empresa1.packfy.com
      /^([^.]+)\.localhost$/,      // empresa1.localhost (desarrollo)
    ];

    for (const pattern of patterns) {
      const match = hostname.match(pattern);
      if (match) {
        const subdomain = match[1];
        // Excluir subdominios administrativos
        if (!['app', 'admin', 'api', 'www'].includes(subdomain)) {
          return subdomain;
        }
      }
    }

    return null;
  };

  const esHostAdministrativo = (hostname: string): boolean => {
    const adminHosts = [
      'app.packfy.com',
      'admin.packfy.com',
      'localhost',
      '127.0.0.1',
    ];
    return adminHosts.includes(hostname);
  };

  // FUNCIONES DE NAVEGACIÓN POR DOMINIOS
  const redirigirAEmpresa = (empresaSlug: string) => {
    const protocol = window.location.protocol;
    let newHost = '';

    // Determinar el host de destino según el entorno
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      // Desarrollo: empresa1.localhost:5173
      const port = window.location.port;
      newHost = port ? `${empresaSlug}.localhost:${port}` : `${empresaSlug}.localhost`;
    } else {
      // Producción: empresa1.packfy.com
      newHost = `${empresaSlug}.packfy.com`;
    }

    const newUrl = `${protocol}//${newHost}${window.location.pathname}${window.location.search}`;
    console.log('🔄 TenantContext: Redirigiendo a empresa:', newUrl);
    window.location.href = newUrl;
  };

  const redirigirAAdmin = () => {
    const protocol = window.location.protocol;
    let newHost = '';

    // Determinar el host administrativo según el entorno
    if (window.location.hostname.includes('localhost') || window.location.hostname.includes('127.0.0.1')) {
      // Desarrollo: localhost:5173
      const port = window.location.port;
      newHost = port ? `localhost:${port}` : 'localhost';
    } else {
      // Producción: app.packfy.com
      newHost = 'app.packfy.com';
    }

    const newUrl = `${protocol}//${newHost}/admin`;
    console.log('🔄 TenantContext: Redirigiendo a admin:', newUrl);
    window.location.href = newUrl;
  };

  // Cargar empresas disponibles para el usuario
  const cargarEmpresas = async (): Promise<void> => {
    try {
      const response = await apiClient.makeRequest('/empresas/');
      const empresasData = response.data as any;
      const empresas = empresasData?.results || empresasData || [];
      setEmpresasDisponibles(Array.isArray(empresas) ? empresas : []);

      console.log(`📊 Empresas cargadas: ${empresas.length}`, empresas);
    } catch (error) {
      console.error('Error cargando empresas:', error);
      setEmpresasDisponibles([]);
    }
  };

  // Cambiar empresa actual
  const cambiarEmpresa = async (empresaSlug: string, empresaData?: Empresa): Promise<void> => {
    try {
      setIsLoading(true);

      // Encontrar la empresa por slug (usar empresaData si se proporciona)
      let empresa = empresaData;
      if (!empresa) {
        empresa = empresasDisponibles.find(e => e.slug === empresaSlug);
      }

      if (!empresa) {
        throw new Error(`Empresa con slug '${empresaSlug}' no encontrada`);
      }

      // Configurar header global para la API
      apiClient.setTenantSlug(empresaSlug);

      // Establecer empresa actual
      setEmpresaActual(empresa);

      // Guardar en localStorage para persistencia
      localStorage.setItem('tenant-slug', empresaSlug);
      localStorage.setItem('empresa-actual', JSON.stringify(empresa));

      // Cargar perfil del usuario en esta empresa
      await obtenerPerfilEnEmpresa();

      console.log(`🏢 Empresa cambiada a: ${empresa.nombre} (${empresaSlug})`);
    } catch (error) {
      console.error('Error cambiando empresa:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Obtener perfil del usuario en la empresa actual
  const obtenerPerfilEnEmpresa = async (): Promise<void> => {
    try {
      const response = await apiClient.makeRequest('/empresas/mis_perfiles/');
      const perfiles = response.data || [];

      // Normalmente debería ser un perfil por empresa, tomar el primero
      const perfil = Array.isArray(perfiles) && perfiles.length > 0 ? perfiles[0] : null;
      setPerfilActual(perfil);

      console.log(`👤 Perfil cargado:`, perfil);
    } catch (error) {
      console.error('Error obteniendo perfil:', error);
      setPerfilActual(null);
    }
  };

  // Verificar si el usuario puede ejecutar una acción
  const puedeEjecutarAccion = (accion: string): boolean => {
    if (!perfilActual) return false;

    const { rol } = perfilActual;

    // Definir permisos por rol
    const permisos: Record<string, string[]> = {
      'dueno': ['*'], // Puede hacer todo
      'operador_miami': ['crear_envio', 'editar_envio', 'cambiar_estado', 'ver_reportes'],
      'operador_cuba': ['cambiar_estado', 'ver_envios', 'actualizar_ubicacion'],
      'remitente': ['crear_envio', 'ver_mis_envios', 'rastrear'],
      'destinatario': ['ver_mis_envios', 'rastrear', 'confirmar_recepcion'],
    };

    const permisosRol = permisos[rol] || [];
    return permisosRol.includes('*') || permisosRol.includes(accion);
  };

  // Verificar si es administrador
  const esAdministrador = (): boolean => {
    return perfilActual?.rol === 'dueno';
  };

  // Inicialización al montar el componente
  useEffect(() => {
    const inicializar = async () => {
      let empresaSeleccionada = false;

      // 1. DETECTAR DOMINIO ACTUAL (NUEVO)
      console.log('🌐 TenantContext: === INICIANDO DETECCIÓN DE DOMINIO ===');
      const empresaDelDominio = detectarDominio();

      if (empresaDelDominio) {
        console.log('🏢 TenantContext: Empresa detectada por subdominio:', empresaDelDominio);

        // Cargar empresas primero para validar
        await cargarEmpresas();

        // Buscar empresa por slug del subdominio
        const empresaEncontrada = empresasDisponibles.find(e => e.slug === empresaDelDominio);

        if (empresaEncontrada) {
          console.log('✅ TenantContext: Empresa válida encontrada:', empresaEncontrada.nombre);
          await cambiarEmpresa(empresaDelDominio, empresaEncontrada);
          empresaSeleccionada = true;
        } else {
          console.warn('⚠️ TenantContext: Empresa del subdominio no encontrada, cargando empresas...');
          // Cargar empresas y buscar nuevamente
          const response = await apiClient.makeRequest('/empresas/');
          const empresasData = response.data as any;
          const empresas = empresasData?.results || empresasData || [];

          const empresaValidada = empresas.find((e: any) => e.slug === empresaDelDominio);
          if (empresaValidada) {
            console.log('✅ TenantContext: Empresa encontrada en segunda búsqueda:', empresaValidada.nombre);
            await cambiarEmpresa(empresaDelDominio, empresaValidada);
            empresaSeleccionada = true;
          } else {
            console.error('❌ TenantContext: Subdominio inválido, redirigiendo a admin...');
            // Redirigir a dominio administrativo si el subdominio no es válido
            setTimeout(() => redirigirAAdmin(), 2000);
            setIsLoading(false);
            return;
          }
        }
      }

      // 2. FALLBACK: Restaurar desde localStorage (solo si no es subdominio)
      if (!empresaSeleccionada && !esSubdominio) {
        const tenantSlug = localStorage.getItem('tenant-slug');
        const empresaGuardada = localStorage.getItem('empresa-actual');

        if (tenantSlug && empresaGuardada) {
          try {
            const empresa = JSON.parse(empresaGuardada);
            setEmpresaActual(empresa);
            apiClient.setTenantSlug(tenantSlug);
            empresaSeleccionada = true;

            // Cargar perfil
            await obtenerPerfilEnEmpresa();
          } catch (error) {
            console.error('Error restaurando empresa:', error);
            // Limpiar localStorage si hay error
            localStorage.removeItem('tenant-slug');
            localStorage.removeItem('empresa-actual');
          }
        }
      }

      // 3. Cargar empresas disponibles (si no se hizo antes)
      if (empresasDisponibles.length === 0) {
        await cargarEmpresas();
      }

      // 4. AUTO-SELECCIÓN: Solo si es dominio admin y no hay empresa
      if (!empresaSeleccionada && esDominioAdmin) {
        const response = await apiClient.makeRequest('/empresas/');
        const empresasData = response.data as any;
        const empresas = empresasData?.results || empresasData || [];

        if (Array.isArray(empresas) && empresas.length > 0) {
          const primeraEmpresa = empresas[0];
          console.log('🏢 Auto-seleccionando primera empresa (admin):', primeraEmpresa.nombre);

          if (primeraEmpresa.slug) {
            // Pasar la empresa directamente para evitar problemas de timing
            await cambiarEmpresa(primeraEmpresa.slug, primeraEmpresa);
          } else {
            console.error('❌ Empresa sin slug:', primeraEmpresa);
          }
        }
      }

      setIsLoading(false);
    };

    // Solo inicializar si hay token de autenticación
    const token = localStorage.getItem('token');
    if (token) {
      inicializar();
    } else {
      setIsLoading(false);
    }
  }, [empresasDisponibles.length, esSubdominio, esDominioAdmin]);

  // Limpiar contexto al logout
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setEmpresaActual(null);
      setPerfilActual(null);
      setEmpresasDisponibles([]);
      localStorage.removeItem('tenant-slug');
      localStorage.removeItem('empresa-actual');
      apiClient.clearTenantSlug();
    }
  }, []);

  const value: TenantContextData = {
    empresaActual,
    perfilActual,
    empresasDisponibles,
    isLoading,
    dominioActual,
    esSubdominio,
    esDominioAdmin,
    cambiarEmpresa,
    cargarEmpresas,
    obtenerPerfilEnEmpresa,
    redirigirAEmpresa,
    redirigirAAdmin,
    puedeEjecutarAccion,
    esAdministrador,
  };

  return (
    <TenantContext.Provider value={value}>
      {children}
    </TenantContext.Provider>
  );
};

// Hook para usar el contexto
export const useTenant = (): TenantContextData => {
  const context = useContext(TenantContext);

  if (!context) {
    throw new Error('useTenant debe usarse dentro de TenantProvider');
  }

  return context;
};

// Hook para verificar permisos
export const usePermissions = () => {
  const { puedeEjecutarAccion, esAdministrador, perfilActual } = useTenant();

  return {
    puede: puedeEjecutarAccion,
    esAdmin: esAdministrador,
    rol: perfilActual?.rol,

    // Shortcuts comunes
    puedeCrearEnvios: () => puedeEjecutarAccion('crear_envio'),
    puedeEditarEnvios: () => puedeEjecutarAccion('editar_envio'),
    puedeCambiarEstados: () => puedeEjecutarAccion('cambiar_estado'),
    puedeVerReportes: () => puedeEjecutarAccion('ver_reportes'),
  };
};
