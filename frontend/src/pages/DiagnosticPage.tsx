import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
// 🇨🇺 CSS ya se importa en main.tsx - sin imports locales

const DiagnosticPage: React.FC = () => {
  const { user, token, isAuthenticated } = useAuth();
  const [apiStatus, setApiStatus] = useState<string>('Probando...');
  const [backendReachable, setBackendReachable] = useState<boolean | null>(null);

  useEffect(() => {
    const testAPI = async () => {
      try {
        console.log('🔍 Diagnóstico: Iniciando pruebas...');
        try {
          // Obtener baseURL desde nuestro cliente
          const cfg = (api as any).getConfig ? (api as any).getConfig() : null;
          console.log('🔍 API Base URL:', cfg?.baseURL || '(no disponible)');
        } catch {}
        console.log('🔍 Token presente:', !!token);
        console.log('🔍 Usuario autenticado:', isAuthenticated);

        // Probar conectividad básica
        // Usar la baseURL del cliente para evitar URLs fijas
        const base = ((api as any).getConfig?.() || {}).baseURL ||
          `${window.location.protocol}//${window.location.hostname}/api`;
        const healthCheck = await fetch(`${base}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (healthCheck.ok) {
          setBackendReachable(true);
          setApiStatus('✅ Backend alcanzable');
          console.log('🔍 Backend responde correctamente');
        } else {
          setBackendReachable(false);
          setApiStatus(`❌ Backend responde con error: ${healthCheck.status}`);
        }

      } catch (error) {
        console.error('🔍 Error en diagnóstico:', error);
        setBackendReachable(false);
        setApiStatus(`❌ Error de conectividad: ${error}`);
      }
    };

    testAPI();
  }, [token, isAuthenticated]);

  return (
    <div className="diagnostic-page">
      <h1>🔍 Página de Diagnóstico</h1>

      <div className="diagnostic-section">
        <h2>Estado de Autenticación</h2>
        <p><strong>Autenticado:</strong> {isAuthenticated ? '✅ Sí' : '❌ No'}</p>
        <p><strong>Token presente:</strong> {token ? '✅ Sí' : '❌ No'}</p>
        {token && (
          <p><strong>Token (primeros 20 chars):</strong> {token.substring(0, 20)}...</p>
        )}
        <p><strong>Usuario:</strong> {user ? `${user.email}` : 'No disponible'}</p>
      </div>

      <div className="diagnostic-section">
        <h2>Estado del Backend</h2>
  <p><strong>URL del API:</strong> {((api as any).getConfig?.() || {}).baseURL || '(no disponible)'}</p>
        <p><strong>Estado:</strong> {apiStatus}</p>
        <p><strong>Alcanzable:</strong> {backendReachable === null ? '⏳ Probando...' : backendReachable ? '✅ Sí' : '❌ No'}</p>
      </div>

      <div className="diagnostic-section">
        <h2>Información del Navegador</h2>
        <p><strong>URL actual:</strong> {window.location.href}</p>
        <p><strong>LocalStorage token:</strong> {localStorage.getItem('token') ? '✅ Presente' : '❌ Ausente'}</p>
        <p><strong>LocalStorage refreshToken:</strong> {localStorage.getItem('refreshToken') ? '✅ Presente' : '❌ Ausente'}</p>
      </div>

      <div className="diagnostic-credentials">
  <h2>Credenciales de Prueba</h2>
  <p><strong>Admin:</strong> admin@packfy.cu / admin123</p>
      </div>
    </div>
  );
};

export default DiagnosticPage;
