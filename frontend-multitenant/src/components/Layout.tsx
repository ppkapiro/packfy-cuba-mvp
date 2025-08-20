import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useTenant } from '../contexts/TenantContext';
import TenantSelector from './TenantSelector';

const Layout = () => {
  const { user, logout } = useAuth();
  const { empresaActual, perfilActual } = useTenant();
  const navigate = useNavigate();
  const location = useLocation();

  console.log('Layout: Renderizando Layout, usuario:', user);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Verificar si la ruta está activa
  const isActiveRoute = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <div className="app-layout">
      <header className="header">
        <div className="header-content">
          <Link to="/dashboard" className="logo">
            <span className="icon icon-flag-cuba icon-lg"></span>
            <span>Packfy Cuba</span>
          </Link>

          {/* Navegación principal */}
          <nav className="nav-main">
            <ul className="nav-menu">
              <li className="nav-item">
                <Link
                  to="/dashboard"
                  className={`nav-link ${isActiveRoute('/dashboard') ? 'active' : ''}`}
                >
                  <span className="icon icon-dashboard"></span>
                  <span>Dashboard</span>
                </Link>
              </li>
              <li className="nav-item">
                <Link
                  to="/envios/nuevo"
                  className={`nav-link ${isActiveRoute('/envios/nuevo') ? 'active' : ''}`}
                >
                  <span className="icon icon-package"></span>
                  <span>Nuevo</span>
                </Link>
              </li>
              <li className="nav-item">
                <Link
                  to="/envios"
                  className={`nav-link ${isActiveRoute('/envios') && !isActiveRoute('/envios/nuevo') ? 'active' : ''}`}
                >
                  <span className="icon icon-package"></span>
                  <span>Gestión</span>
                </Link>
              </li>
              <li className="nav-item">
                <Link
                  to="/rastreo"
                  className={`nav-link ${isActiveRoute('/rastreo') ? 'active' : ''}`}
                  onClick={() => console.log('🔍 Layout: Navegando a /rastreo')}
                >
                  <span className="icon icon-search"></span>
                  <span>Rastrear</span>
                </Link>
              </li>
            </ul>
          </nav>

          {/* Selector de empresa */}
          <div className="tenant-section">
            <TenantSelector />
          </div>

          {/* Menú de usuario */}
          <div className="user-menu">
            {user ? (
              <div className="user-info">
                <span className="user-name">
                  {user.nombre || user.email?.split('@')[0]}
                </span>
                <button onClick={handleLogout} className="nav-link">
                  <span className="icon icon-user"></span>
                  <span>Salir</span>
                </button>
              </div>
            ) : (
              <Link to="/login" className="nav-link">
                <span className="icon icon-user"></span>
                <span>Entrar</span>
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Sección de información del tenant */}
      {empresaActual && (
        <section className="layout-tenant-section">
          <div className="layout-tenant-container">
            <div className="layout-tenant-info">
              <div className="layout-tenant-logo">
                {empresaActual.nombre.substring(0, 2).toUpperCase()}
              </div>
              <div className="layout-tenant-details">
                <h2 className="layout-tenant-name">{empresaActual.nombre}</h2>
                <p className="layout-tenant-role">
                  <span>Trabajando como:</span>
                  <span className="layout-tenant-role-badge">
                    {perfilActual?.rol === 'dueno' ? 'Dueño' :
                     perfilActual?.rol === 'operador_miami' ? 'Operador Miami' :
                     perfilActual?.rol === 'operador_cuba' ? 'Operador Cuba' :
                     perfilActual?.rol === 'remitente' ? 'Remitente' :
                     perfilActual?.rol === 'destinatario' ? 'Destinatario' : 'Usuario'}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </section>
      )}

      <main className="app-content">
        <div className="container">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;
