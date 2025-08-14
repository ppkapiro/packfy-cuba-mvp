import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

// 🇨🇺 LOGIN UNIFICADO - Sin CSS personalizado, con CSS Master

const LoginPage: React.FC = () => {
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
        const win = window as Window;
        win.location.href = '/dashboard';
      }, 300);

    } catch (err: any) {
      console.error('LoginPage: Error al iniciar sesión:', err);

      if (err.response) {
        console.error('LoginPage: Error de respuesta:', err.response.status, err.response.statusText);
        console.error('LoginPage: Datos del error:', err.response.data);

        // Mensajes de error más descriptivos
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
    <div className="login-page-container">
      {/* Hero Section con identidad cubana */}
      <div className="login-hero">
        <div className="login-hero-content">
          <div className="login-brand">
            <div className="login-logo">🇨🇺</div>
            <h1 className="login-title">Packfy Cuba</h1>
            <p className="login-subtitle">
              Sistema Moderno de Paquetería
            </p>
          </div>

          <div className="login-features">
            <div className="login-feature">
              <span className="feature-icon">📦</span>
              <span>Gestión completa de envíos</span>
            </div>
            <div className="login-feature">
              <span className="feature-icon">🚚</span>
              <span>Seguimiento en tiempo real</span>
            </div>
            <div className="login-feature">
              <span className="feature-icon">💰</span>
              <span>Precios competitivos</span>
            </div>
            <div className="login-feature">
              <span className="feature-icon">🇨🇺</span>
              <span>Hecho en Cuba para cubanos</span>
            </div>
          </div>
        </div>
      </div>

      {/* Formulario de login */}
      <div className="login-form-container">
        <div className="login-form-card">

          {/* Header del formulario */}
          <div className="login-form-header">
            <h2 className="login-form-title">Iniciar Sesión</h2>
            <p className="login-form-subtitle">
              Accede a tu cuenta para gestionar tus envíos
            </p>
          </div>

          {/* Error message */}
          {error && (
            <div className="alert alert-error">
              <span>{error}</span>
              <button
                className="close-button"
                onClick={() => setError('')}
              >
                ✕
              </button>
            </div>
          )}

          {/* Formulario */}
          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label className="form-label">
                📧 Correo Electrónico
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-control"
                placeholder="tu@email.com"
                required
                disabled={loading}
                aria-label="Correo electrónico"
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                🔒 Contraseña
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-control"
                placeholder="••••••••"
                required
                disabled={loading}
                aria-label="Contraseña"
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-lg login-submit-btn"
              disabled={loading || !email || !password}
            >
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  Iniciando sesión...
                </>
              ) : (
                <>
                  🚀 Iniciar Sesión
                </>
              )}
            </button>
          </form>

          {/* Enlaces adicionales */}
          <div className="login-form-footer">
            <div className="login-links">
              <a href="#" className="login-link">
                ❓ ¿Olvidaste tu contraseña?
              </a>
              <a href="#" className="login-link">
                📞 Contactar soporte
              </a>
            </div>

            <div className="login-info">
              <p className="text-muted text-center">
                Para obtener una cuenta, contacta al administrador del sistema.
              </p>
            </div>
          </div>
        </div>

        {/* Información del sistema */}
        <div className="login-system-info">
          <div className="system-stats">
            <div className="system-stat">
              <span className="stat-icon">🌟</span>
              <span className="stat-text">Sistema en línea</span>
            </div>
            <div className="system-stat">
              <span className="stat-icon">🔒</span>
              <span className="stat-text">Conexión segura</span>
            </div>
            <div className="system-stat">
              <span className="stat-icon">⚡</span>
              <span className="stat-text">Respuesta rápida</span>
            </div>
          </div>

          <div className="login-version">
            <p className="text-muted">
              Packfy Cuba v4.0 - Sistema de Paquetería Moderno
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
