import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTenant } from '../contexts/TenantContext';
import RemitenteForm from './envios/RemitenteForm';
import OperadorForm from './envios/OperadorForm';
import AdminForm from './envios/AdminForm';
import DestinatarioView from './envios/DestinatarioView';
import { AlertCircle, Package } from 'lucide-react';

/**
 * Contenedor principal para formularios de envío
 * Decide qué vista mostrar según el rol del usuario autenticado
 */
const EnvioFormContainer: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const { currentTenant } = useTenant();

  // Verificar autenticación
  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
            <AlertCircle className="w-6 h-6 text-red-600" />
          </div>
          <div className="text-center">
            <h2 className="text-lg font-medium text-gray-900 mb-2">
              Acceso Requerido
            </h2>
            <p className="text-sm text-gray-600">
              Debes iniciar sesión para acceder a esta funcionalidad.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Verificar tenant
  if (!currentTenant) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-center w-12 h-12 mx-auto bg-amber-100 rounded-full mb-4">
            <Package className="w-6 h-6 text-amber-600" />
          </div>
          <div className="text-center">
            <h2 className="text-lg font-medium text-gray-900 mb-2">
              Empresa Requerida
            </h2>
            <p className="text-sm text-gray-600">
              Debes seleccionar una empresa para gestionar envíos.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Obtener perfil activo para el tenant actual
  const perfilActivo = user.perfiles_empresa?.find(
    perfil => perfil.empresa.slug === currentTenant.slug && perfil.activo
  );

  if (!perfilActivo) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-center w-12 h-12 mx-auto bg-gray-100 rounded-full mb-4">
            <Package className="w-6 h-6 text-gray-600" />
          </div>
          <div className="text-center">
            <h2 className="text-lg font-medium text-gray-900 mb-2">
              Sin Permisos
            </h2>
            <p className="text-sm text-gray-600">
              No tienes permisos para gestionar envíos en esta empresa.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Decidir qué componente renderizar según el rol
  const rol = perfilActivo.rol;

  switch (rol) {
    case 'dueno':
      return <AdminForm user={user} tenant={currentTenant} perfil={perfilActivo} />;

    case 'operador_miami':
    case 'operador_cuba':
      return <OperadorForm user={user} tenant={currentTenant} perfil={perfilActivo} />;

    case 'remitente':
      return <RemitenteForm user={user} tenant={currentTenant} perfil={perfilActivo} />;

    case 'destinatario':
      return <DestinatarioView user={user} tenant={currentTenant} perfil={perfilActivo} />;

    default:
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-gray-100 rounded-full mb-4">
              <AlertCircle className="w-6 h-6 text-gray-600" />
            </div>
            <div className="text-center">
              <h2 className="text-lg font-medium text-gray-900 mb-2">
                Rol No Reconocido
              </h2>
              <p className="text-sm text-gray-600">
                Tu rol "{rol}" no tiene una vista específica configurada.
              </p>
            </div>
          </div>
        </div>
      );
  }
};

export default EnvioFormContainer;
