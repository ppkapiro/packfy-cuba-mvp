import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTenant } from '../contexts/TenantContext';

const NavigationDebugInfo: React.FC = () => {
  const { user } = useAuth();
  const { empresaActual, perfilActual } = useTenant();

  // Solo mostrar en desarrollo
  if (process.env.NODE_ENV !== 'development') {
    return null;
  }

  return (
    <div className="fixed top-0 right-0 bg-black bg-opacity-80 text-white p-2 text-xs z-50 max-w-xs rounded-bl-lg font-mono">
      <h4>🔍 DEBUG - NAVEGACIÓN</h4>

      <div><strong>Usuario:</strong></div>
      <div>ID: {user?.id || 'No ID'}</div>
      <div>Email: {user?.email || 'No email'}</div>
      <div>Nombre: {user?.nombre || 'No nombre'}</div>

      <div><strong>Empresa:</strong></div>
      <div>ID: {empresaActual?.id || 'No empresa'}</div>
      <div>Nombre: {empresaActual?.nombre || 'No nombre'}</div>

      <div><strong>Perfil:</strong></div>
      <div>
        Rol: {perfilActual?.rol || 'No rol'}
      </div>

      <div><strong>Navegación:</strong></div>
      <div>
        {perfilActual?.rol === 'dueno' ? '✅ AdminNavigation' : '📋 StandardNavigation'}
      </div>

      {perfilActual?.rol === 'dueno' && (
        <div>
          🎯 Dashboard: /admin/dashboard
        </div>
      )}
    </div>
  );
};

export default NavigationDebugInfo;
