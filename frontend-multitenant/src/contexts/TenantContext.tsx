import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiClient from '../services/api';
import { useAuth } from './AuthContext';

// Tipos para el sistema multi-tenant
interface Empresa {
  id: number;
  nombre: string;
  slug: string;
  rol?: string;  // Agregado para el rol del usuario en la empresa
}

interface PerfilUsuario {
  rol: 'dueno' | 'operador_miami' | 'operador_cuba' | 'remitente' | 'destinatario';
  fecha_ingreso?: string;
  configuracion?: Record<string, any>;
}

interface TenantContextData {
  // Estado actual
  empresaActual: Empresa | null;
  perfilActual: PerfilUsuario | null;
  empresasDisponibles: Empresa[];
  isLoading: boolean;

  // Acciones
  cambiarEmpresa: (empresaSlug: string) => Promise<void>;
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
  const { isAuthenticated, user } = useAuth();
  const [empresaActual, setEmpresaActual] = useState<Empresa | null>(null);
  const [perfilActual, setPerfilActual] = useState<PerfilUsuario | null>(null);
  const [empresasDisponibles, setEmpresasDisponibles] = useState<Empresa[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Cargar empresas disponibles para el usuario
  const cargarEmpresas = async (): Promise<void> => {
    try {
      console.log('🔄 TenantContext: Cargando empresas del usuario...');

      // Obtener empresas desde el perfil del usuario
      const response = await apiClient.makeRequest('/usuarios/me/');

      console.log('👤 TenantContext: Respuesta raw:', response);

      if (response.status !== 200) {
        console.error('❌ TenantContext: Error en respuesta:', response.error);
        setEmpresasDisponibles([]);
        return;
      }

      const userData = response.data;
      console.log('👤 TenantContext: Datos del usuario:', userData);

      // Extraer empresas del usuario con validación
      const empresas = userData?.empresas;

      if (!Array.isArray(empresas)) {
        console.warn('⚠️ TenantContext: empresas no es un array:', empresas);
        setEmpresasDisponibles([]);
        return;
      }

      console.log('🏢 TenantContext: Empresas encontradas:', empresas);

      if (empresas.length > 0) {
        setEmpresasDisponibles(empresas);
        console.log(`✅ TenantContext: ${empresas.length} empresas cargadas`);

        // Si hay empresas y no hay una seleccionada, seleccionar la primera
        if (!empresaActual) {
          const primeraEmpresa = empresas[0];
          console.log('🎯 TenantContext: Seleccionando primera empresa:', primeraEmpresa.nombre);
          try {
            await cambiarEmpresa(primeraEmpresa.slug);
          } catch (cambioError) {
            console.error('❌ TenantContext: Error cambiando a primera empresa:', cambioError);
          }
        }
      } else {
        console.warn('⚠️ TenantContext: Usuario sin empresas asignadas');
        setEmpresasDisponibles([]);
      }
    } catch (error) {
      console.error('❌ TenantContext: Error cargando empresas:', error);
      setEmpresasDisponibles([]);
    }
  };  // Cambiar empresa actual
  const cambiarEmpresa = async (empresaSlug: string): Promise<void> => {
    try {
      setIsLoading(true);

      // Encontrar la empresa por slug
      const empresa = empresasDisponibles.find(e => e.slug === empresaSlug);
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
      if (!empresaActual) {
        console.warn('⚠️ TenantContext: No hay empresa actual para obtener perfil');
        return;
      }

      // El rol ya está en los datos de la empresa del usuario
      const empresaCompleta = empresasDisponibles.find(e => e.slug === empresaActual.slug);
      if (empresaCompleta?.rol) {
        const perfil: PerfilUsuario = {
          rol: empresaCompleta.rol as any,
          fecha_ingreso: new Date().toISOString(), // Temporal
        };
        setPerfilActual(perfil);
        console.log(`👤 TenantContext: Perfil establecido:`, perfil);
      } else {
        console.warn('⚠️ TenantContext: No se encontró rol para la empresa actual');
        setPerfilActual(null);
      }
    } catch (error) {
      console.error('❌ TenantContext: Error obteniendo perfil:', error);
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
      console.log('🔄 TenantContext: Iniciando inicialización...');
      console.log('👤 TenantContext: Usuario autenticado:', isAuthenticated);
      console.log('📋 TenantContext: Datos de usuario:', user);

      // Intentar restaurar empresa desde localStorage
      const tenantSlug = localStorage.getItem('tenant-slug');
      const empresaGuardada = localStorage.getItem('empresa-actual');

      if (tenantSlug && empresaGuardada) {
        try {
          const empresa = JSON.parse(empresaGuardada);
          setEmpresaActual(empresa);
          apiClient.setTenantSlug(tenantSlug);

          // Cargar perfil
          await obtenerPerfilEnEmpresa();
        } catch (error) {
          console.error('❌ TenantContext: Error restaurando empresa:', error);
          // Limpiar localStorage si hay error
          localStorage.removeItem('tenant-slug');
          localStorage.removeItem('empresa-actual');
        }
      }

      // Cargar empresas disponibles
      await cargarEmpresas();
      setIsLoading(false);
    };

    // Solo inicializar si el usuario está autenticado
    if (isAuthenticated && user) {
      console.log('✅ TenantContext: Usuario autenticado, iniciando...');
      inicializar();
    } else if (isAuthenticated === false) {
      // Usuario no autenticado, limpiar estado
      console.log('🚫 TenantContext: Usuario no autenticado, limpiando estado...');
      setEmpresaActual(null);
      setPerfilActual(null);
      setEmpresasDisponibles([]);
      localStorage.removeItem('tenant-slug');
      localStorage.removeItem('empresa-actual');
      apiClient.clearTenantSlug();
      setIsLoading(false);
    } else {
      // isAuthenticated puede ser null durante la carga inicial
      console.log('⏳ TenantContext: Esperando estado de autenticación...');
      setIsLoading(true);
    }
  }, [isAuthenticated, user]);

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
