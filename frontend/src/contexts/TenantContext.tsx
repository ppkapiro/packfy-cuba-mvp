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

  // Acciones
  cambiarEmpresa: (empresaSlug: string, empresaData?: Empresa) => Promise<void>;
  cargarEmpresas: () => Promise<void>;
  obtenerPerfilEnEmpresa: () => Promise<void>;

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

  // Cargar empresas disponibles para el usuario
  const cargarEmpresas = async (): Promise<void> => {
    try {
      const response = await apiClient.makeRequest('/empresas/');
      const empresasData = response.data as any;
      const empresas = empresasData?.results || empresasData || [];
      setEmpresasDisponibles(Array.isArray(empresas) ? empresas : []);

      // FIJO: Evitar loop infinito - solo auto-seleccionar en inicialización
      // Esto se manejará en el useEffect de inicialización
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

      // Intentar restaurar empresa desde localStorage
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

      // Cargar empresas disponibles
      await cargarEmpresas();

      // Si no hay empresa seleccionada, seleccionar la primera disponible
      if (!empresaSeleccionada) {
        const response = await apiClient.makeRequest('/empresas/');
        const empresasData = response.data as any;
        const empresas = empresasData?.results || empresasData || [];

        if (Array.isArray(empresas) && empresas.length > 0) {
          const primeraEmpresa = empresas[0];
          console.log('🏢 Auto-seleccionando primera empresa:', primeraEmpresa.nombre);
          console.log('📊 Estructura completa de empresa:', primeraEmpresa);
          console.log('🔑 Slug de empresa:', primeraEmpresa.slug);

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
  }, []);

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
    cambiarEmpresa,
    cargarEmpresas,
    obtenerPerfilEnEmpresa,
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
