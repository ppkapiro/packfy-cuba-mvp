import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Empresa, PerfilUsuario } from '../types';
import { useAuth } from './AuthContext';
import apiClient from '../services/api';

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
      console.log('🔑 TenantContext: Estado de autenticación:', isAuthenticated);
      console.log('👤 TenantContext: Usuario actual:', user);

      // Obtener empresas desde el perfil del usuario
      const response = await apiClient.makeRequest('/usuarios/me/');

      console.log('👤 TenantContext: Respuesta raw completa:', response);
      console.log('📊 TenantContext: Status:', response.status);
      console.log('📄 TenantContext: Data:', response.data);
      console.log('❌ TenantContext: Error:', response.error);

      if (response.status !== 200 || response.error) {
        console.error('❌ TenantContext: Error en respuesta:', response.error);
        console.error('❌ TenantContext: Status code:', response.status);
        setEmpresasDisponibles([]);
        return;
      }

      const userData = response.data;
      console.log('👤 TenantContext: Datos del usuario completos:', userData);
      console.log('👤 TenantContext: Tipo de userData:', typeof userData);
      console.log('👤 TenantContext: Keys de userData:', Object.keys(userData || {}));

      // Extraer empresas del usuario con validación
      const empresas = (userData as any)?.empresas || (userData as any)?.companies || [];

      console.log('🏢 TenantContext: Empresas extraídas:', empresas);
      console.log('🏢 TenantContext: Tipo de empresas:', typeof empresas);
      console.log('🏢 TenantContext: Es array?:', Array.isArray(empresas));

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
          console.log('🎯 TenantContext: Seleccionando primera empresa:', primeraEmpresa.name);
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

      console.log(`🏢 Empresa cambiada a: ${empresa.name} (${empresaSlug})`);
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

      // Buscar el rol en los perfiles de la empresa
      const empresaCompleta = empresasDisponibles.find(e => e.slug === empresaActual.slug);
      console.log('🔍 TenantContext: Empresa completa encontrada:', empresaCompleta);

      if (empresaCompleta) {
        // Buscar perfil activo del usuario en esta empresa
        const perfiles = empresaCompleta.perfiles || [];
        console.log('📋 TenantContext: Perfiles en empresa:', perfiles);

        const perfilActivo = perfiles.find((p: any) => p.is_active === true);
        console.log('🎯 TenantContext: Perfil activo encontrado:', perfilActivo);

        if (perfilActivo) {
          const perfil: PerfilUsuario = {
            id: perfilActivo.id || 1,
            usuario: perfilActivo.usuario || 'current-user',
            rol: perfilActivo.rol as any,
            empresa: empresaCompleta.id,
            fecha_ingreso: perfilActivo.fecha_ingreso || new Date().toISOString(),
          };
          setPerfilActual(perfil);
          console.log(`✅ TenantContext: Perfil establecido correctamente:`, perfil);
        } else {
          console.warn('⚠️ TenantContext: No se encontró perfil activo para la empresa actual');
          console.log('📋 TenantContext: Perfiles disponibles:', perfiles);
          setPerfilActual(null);
        }
      } else {
        console.warn('⚠️ TenantContext: No se encontró empresa completa');
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
      console.log('🔄 TenantContext: === INICIANDO INICIALIZACIÓN ===');
      console.log('👤 TenantContext: Usuario autenticado:', isAuthenticated);
      console.log('📋 TenantContext: Datos de usuario:', user);
      console.log('🏢 TenantContext: Empresas disponibles actuales:', empresasDisponibles.length);
      console.log('⏳ TenantContext: Estado isLoading:', isLoading);

      // Intentar restaurar empresa desde localStorage
      const tenantSlug = localStorage.getItem('tenant-slug');
      const empresaGuardada = localStorage.getItem('empresa-actual');

      console.log('💾 TenantContext: TenantSlug en localStorage:', tenantSlug);
      console.log('💾 TenantContext: Empresa guardada en localStorage:', empresaGuardada);

      if (tenantSlug && empresaGuardada) {
        try {
          const empresa = JSON.parse(empresaGuardada);
          console.log('🏢 TenantContext: Restaurando empresa:', empresa);
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

      // Cargar empresas disponibles (optimizado para evitar loops)
      await cargarEmpresas();
      setIsLoading(false);
    };

    // Solo inicializar si el usuario está autenticado y no hemos cargado empresas
    if (isAuthenticated && user && empresasDisponibles.length === 0) {
      console.log('✅ TenantContext: === CONDICIÓN CUMPLIDA - INICIANDO ===');
      console.log('✅ TenantContext: isAuthenticated:', isAuthenticated);
      console.log('✅ TenantContext: user existe:', !!user);
      console.log('✅ TenantContext: empresasDisponibles.length:', empresasDisponibles.length);
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
      console.log('⏳ TenantContext: === ESPERANDO ESTADO DE AUTENTICACIÓN ===');
      console.log('⏳ TenantContext: isAuthenticated:', isAuthenticated);
      console.log('⏳ TenantContext: user existe:', !!user);
      console.log('⏳ TenantContext: empresasDisponibles.length:', empresasDisponibles.length);
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
