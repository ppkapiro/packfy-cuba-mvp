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
    return (
    <div className="login-page">
      <div className="login-container">
        <h1>Paquetería Cuba</h1>
        <h2>Iniciar Sesión</h2>
        
        {error && (
          <div className="alert alert-error">
            <div className="error-icon">⚠️</div>
            <div className="error-message">{error}</div>
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Correo Electrónico</label>
            <input
              type="email"
              id="email"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
            <button
            type="submit"
            className="btn btn-block"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="loading-spinner"></span>
                Iniciando sesión...
              </>
            ) : 'Iniciar Sesión'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;