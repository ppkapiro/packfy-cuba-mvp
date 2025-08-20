import React, { useEffect, useState } from 'react';

const StatusSystem: React.FC = () => {
  const [status, setStatus] = useState<{
    backend: 'checking' | 'online' | 'offline';
    frontend: 'online';
    auth: 'checking' | 'working' | 'error';
  }>({
    backend: 'checking',
    frontend: 'online',
    auth: 'checking'
  });

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/health/', {
          method: 'GET',
          mode: 'cors'
        });
        setStatus(prev => ({
          ...prev,
          backend: response.ok ? 'online' : 'offline'
        }));
      } catch (error) {
        console.error('Backend check failed:', error);
        setStatus(prev => ({
          ...prev,
          backend: 'offline'
        }));
      }
    };

    const checkAuth = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: 'admin@packfy.com',
            password: 'admin123'
          })
        });

        setStatus(prev => ({
          ...prev,
          auth: response.ok ? 'working' : 'error'
        }));
      } catch (error) {
        console.error('Auth check failed:', error);
        setStatus(prev => ({
          ...prev,
          auth: 'error'
        }));
      }
    };

    checkBackend();
    checkAuth();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
      case 'working': return '#28a745';
      case 'offline':
      case 'error': return '#dc3545';
      case 'checking': return '#ffc107';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'online': return '✅ En línea';
      case 'working': return '✅ Funcionando';
      case 'offline': return '❌ Desconectado';
      case 'error': return '❌ Error';
      case 'checking': return '🔄 Verificando...';
      default: return '❓ Desconocido';
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: '10px',
      right: '10px',
      background: 'white',
      border: '1px solid #ccc',
      borderRadius: '8px',
      padding: '15px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      fontFamily: 'monospace',
      fontSize: '12px',
      zIndex: 9999
    }}>
      <h4 style={{ margin: '0 0 10px 0' }}>🔍 Estado del Sistema</h4>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: getStatusColor(status.frontend) }}>
          {getStatusText(status.frontend)}
        </span>
        <span style={{ marginLeft: '10px' }}>Frontend</span>
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: getStatusColor(status.backend) }}>
          {getStatusText(status.backend)}
        </span>
        <span style={{ marginLeft: '10px' }}>Backend API</span>
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: getStatusColor(status.auth) }}>
          {getStatusText(status.auth)}
        </span>
        <span style={{ marginLeft: '10px' }}>Autenticación</span>
      </div>

      <div style={{ marginTop: '10px', fontSize: '10px', color: '#666' }}>
        URL: {window.location.href}
      </div>
    </div>
  );
};

export default StatusSystem;
