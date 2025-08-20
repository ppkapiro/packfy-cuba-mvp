import React, { useState } from 'react';
import { authAPI } from '../services/api';

const LoginTest: React.FC = () => {
  const [email, setEmail] = useState('superadmin@packfy.com');
  const [password, setPassword] = useState('super123!');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Credenciales predefinidas para testing
  const credentials = [
    { name: 'Superadmin', email: 'superadmin@packfy.com', password: 'super123!' },
    { name: 'Dueño', email: 'dueno@packfy.com', password: 'dueno123!' },
    { name: 'Miami', email: 'miami@packfy.com', password: 'miami123!' },
    { name: 'Cuba', email: 'cuba@packfy.com', password: 'cuba123!' },
    { name: 'Remitente1', email: 'remitente1@packfy.com', password: 'remitente123!' },
    { name: 'Destinatario1', email: 'destinatario1@cuba.cu', password: 'destinatario123!' },
  ];

  const testLogin = async () => {
    setLoading(true);
    setResult(null);

    try {
      console.log('🔑 Testing login with:', { email, password });

      const response = await authAPI.login(email, password);

      console.log('✅ Login response:', response);
      setResult({
        success: true,
        data: response
      });
    } catch (error) {
      console.error('❌ Login error:', error);
      setResult({
        success: false,
        error: error
      });
    } finally {
      setLoading(false);
    }
  };

  const testMe = async () => {
    setLoading(true);

    try {
      const response = await fetch('/api/usuarios/me/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      console.log('👤 Me response:', data);
      setResult({
        success: response.ok,
        data: data
      });
    } catch (error) {
      console.error('❌ Me error:', error);
      setResult({
        success: false,
        error: error
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px', margin: '0 auto' }}>
      <h1>🧪 Test de Login</h1>

      {/* Botones de credenciales rápidas */}
      <div style={{ marginBottom: '20px' }}>
        <h3>Credenciales Rápidas:</h3>
        {credentials.map((cred, index) => (
          <button
            key={index}
            onClick={() => {setEmail(cred.email); setPassword(cred.password);}}
            style={{
              padding: '5px 10px',
              margin: '5px',
              fontSize: '12px',
              backgroundColor: email === cred.email ? '#007bff' : '#f8f9fa',
              color: email === cred.email ? 'white' : 'black',
              border: '1px solid #ccc',
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            {cred.name}
          </button>
        ))}
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
          />
        </label>

        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={testLogin}
          disabled={loading}
          style={{ padding: '10px 20px', marginRight: '10px' }}
        >
          {loading ? 'Testing...' : 'Test Login'}
        </button>

        <button
          onClick={testMe}
          disabled={loading}
          style={{ padding: '10px 20px' }}
        >
          Test /usuarios/me/
        </button>
      </div>

      {result && (
        <div style={{
          padding: '15px',
          borderRadius: '5px',
          backgroundColor: result.success ? '#d4edda' : '#f8d7da',
          border: `1px solid ${result.success ? '#c3e6cb' : '#f5c6cb'}`
        }}>
          <h3>{result.success ? '✅ Success' : '❌ Error'}</h3>
          <pre style={{ fontSize: '12px', overflow: 'auto' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default LoginTest;
