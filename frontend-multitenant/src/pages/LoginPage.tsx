import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    console.log('LoginPage: Iniciando sesión con email:', email);
    try {
      await login(email, password);
      console.log('LoginPage: Inicio de sesión exitoso, redirigiendo a /dashboard');
      // Pequeña pausa antes de redireccionar
      setTimeout(() => {
        // Usar window.location.href en lugar de navigate para garantizar una carga fresca
        const win = window as Window;
        win.location.href = '/dashboard';
      }, 300);
    } catch (err: any) {
      console.error('LoginPage: Error al iniciar sesión:', err);

      if (err.response) {
        console.error('LoginPage: Error de respuesta:', err.response.status, err.response.statusText);
        console.error('LoginPage: Datos del error:', err.response.data);

        // Mensajes de error más descriptivos según el código de respuesta
        if (err.response.status === 401) {
          setError('Credenciales incorrectas. Por favor, verifica tu correo y contraseña.');
        } else if (err.response.status === 403) {
          setError('Tu cuenta no tiene permisos para acceder. Contacta al administrador.');
        } else if (err.response.status >= 500) {
          setError('Error en el servidor. Por favor, intenta más tarde o contacta al soporte técnico.');
        } else {
          setError(err.response?.data?.detail || `Error ${err.response.status}: ${err.response.statusText}`);
        }
      } else if (err.request) {
        console.error('LoginPage: No se recibió respuesta del servidor');
        setError('No se pudo conectar con el servidor. Verifica tu conexión a internet e intenta nuevamente.');
      } else {
        console.error('LoginPage: Error desconocido:', err.message);
        setError('Error al iniciar sesión: ' + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  // Función para autocompletar credenciales de prueba
  const fillTestCredentials = (testEmail: string, testPassword: string) => {
    setEmail(testEmail);
    setPassword(testPassword);
    setError('');
  };

  return (
    <div className="login-page">
      <div className="form-container">
        <div className="form-header">
          <div className="login-logo">
            <span className="icon icon-flag-cuba icon-2xl"></span>
          </div>
          <h1 className="form-title">Packfy Cuba</h1>
          <p className="form-subtitle">Sistema de Paquetería Moderno</p>
        </div>

        {error && (
          <div className="form-error">
            <span className="icon icon-close"></span>
            <span>{error}</span>
          </div>
        )}

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Correo Electrónico
            </label>
            <div className="form-input-with-icon">
              <input
                type="email"
                id="email"
                className="form-input"
                placeholder="ejemplo@packfy.cu"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
              <span className="form-input-icon icon icon-user"></span>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Contraseña
            </label>
            <div className="form-input-with-icon">
              <input
                type="password"
                id="password"
                className="form-input"
                placeholder="Tu contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
              <span className="form-input-icon icon icon-close"></span>
            </div>
          </div>

          <div className="form-button-group">
            <button
              type="submit"
              className="form-button form-button-primary"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  <span>Iniciando...</span>
                </>
              ) : (
                <>
                  <span className="icon icon-user"></span>
                  <span>Iniciar Sesión</span>
                </>
              )}
            </button>
          </div>
        </form>

        <div className="login-divider"></div>

        {/* Credenciales de prueba para desarrollo */}
        <div className="test-credentials">
          <div className="test-credentials-title">
            🧪 Credenciales de Prueba Validadas
          </div>

          <div
            className="test-credential"
            onClick={() => fillTestCredentials('admin@packfy.com', 'admin123')}
          >
            <span>👑 Superadmin</span>
            <span>admin@packfy.com</span>
          </div>

          <div
            className="test-credential"
            onClick={() => fillTestCredentials('dueno@packfy.com', 'password123')}
          >
            <span>🏢 Dueño Principal</span>
            <span>dueno@packfy.com</span>
          </div>

          <div
            className="test-credential"
            onClick={() => fillTestCredentials('consultor@packfy.com', 'password123')}
          >
            <span>� Multi-empresa</span>
            <span>consultor@packfy.com</span>
          </div>

          <div
            className="test-credential"
            onClick={() => fillTestCredentials('demo@packfy.com', 'demo123')}
          >
            <span>🧪 Demo Multi</span>
            <span>demo@packfy.com</span>
          </div>

          <div
            className="test-credential"
            onClick={() => fillTestCredentials('miami@packfy.com', 'password123')}
          >
            <span>🚚 Operador Miami</span>
            <span>miami@packfy.com</span>
          </div>

          <div
            className="test-credential"
            onClick={() => fillTestCredentials('cuba@packfy.com', 'password123')}
          >
            <span>🇨🇺 Operador Cuba</span>
            <span>cuba@packfy.com</span>
          </div>
        </div>

        <div className="login-footer">
          <div className="login-links">
            <a href="/rastrear" className="login-link">
              🔍 Rastrear Paquete sin Registro
            </a>
            <a href="#" className="login-link">
              ❓ ¿Olvidaste tu contraseña?
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
