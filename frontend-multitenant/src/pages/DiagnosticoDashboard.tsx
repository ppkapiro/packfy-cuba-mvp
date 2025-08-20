import React from 'react';
import { useTenant } from '../contexts/TenantContext';
import { useAuth } from '../contexts/AuthContext';

const DiagnosticoDashboard: React.FC = () => {
  const { perfilActual, empresaActual, empresasDisponibles, isLoading } = useTenant();
  const { user, isAuthenticated } = useAuth();

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>🔍 Diagnóstico del Dashboard</h1>

      <div style={{ marginBottom: '20px' }}>
        <h2>📊 Estado de Autenticación</h2>
        <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
{JSON.stringify({
  isAuthenticated,
  user: user ? {
    id: user.id,
    email: user.email
  } : null
}, null, 2)}
        </pre>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h2>🏢 Estado del Tenant</h2>
        <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
{JSON.stringify({
  isLoading,
  empresaActual,
  perfilActual,
  empresasDisponibles: empresasDisponibles?.length || 0,
  empresasDisponiblesData: empresasDisponibles
}, null, 2)}
        </pre>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h2>💾 LocalStorage</h2>
        <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
{JSON.stringify({
  'access_token': localStorage.getItem('access_token') ? 'EXISTS' : null,
  'refresh_token': localStorage.getItem('refresh_token') ? 'EXISTS' : null,
  'tenant-slug': localStorage.getItem('tenant-slug'),
  'empresa-actual': localStorage.getItem('empresa-actual')
}, null, 2)}
        </pre>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h2>🚨 Problema Identificado</h2>
        <div style={{
          backgroundColor: perfilActual ? '#d4edda' : '#f8d7da',
          color: perfilActual ? '#155724' : '#721c24',
          padding: '15px',
          borderRadius: '5px',
          border: `1px solid ${perfilActual ? '#c3e6cb' : '#f5c6cb'}`
        }}>
          {perfilActual ? (
            <div>
              <strong>✅ Perfil cargado correctamente</strong>
              <p>Rol: {perfilActual.rol}</p>
              <p>Empresa: {empresaActual?.name}</p>
            </div>
          ) : (
            <div>
              <strong>❌ Sin perfil de usuario</strong>
              <p>Causa probable:</p>
              <ul>
                <li>TenantContext no está ejecutando cargarEmpresas()</li>
                <li>API /usuarios/me/ no devuelve empresas</li>
                <li>Usuario no tiene perfiles asignados</li>
                <li>Error en la estructura de datos</li>
              </ul>
            </div>
          )}
        </div>
      </div>

      <div>
        <h2>🔧 Acciones de Diagnóstico</h2>
        <button
          onClick={() => window.location.reload()}
          style={{ padding: '10px 20px', margin: '5px' }}
        >
          🔄 Recargar Página
        </button>

        <button
          onClick={() => {
            localStorage.clear();
            window.location.href = '/login';
          }}
          style={{ padding: '10px 20px', margin: '5px' }}
        >
          🧹 Limpiar y Re-login
        </button>
      </div>
    </div>
  );
};

export default DiagnosticoDashboard;
