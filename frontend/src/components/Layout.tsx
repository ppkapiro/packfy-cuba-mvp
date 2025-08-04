import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { InstallPWAButton } from './InstallPWAButton';

const Layout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  console.log('Layout: Renderizando Layout, usuario:', user);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  return (
    <div className="app-layout">
      <header className="app-header">
        <div className="container">
          <div className="logo">
            <h1>Paquetería Cuba</h1>
          </div>          <nav className="main-nav">
            <ul>
              <li><Link to="/dashboard">Dashboard</Link></li>
              <li><Link to="/envios/nuevo">Nuevo Envío</Link></li>
              <li><Link to="/seguimiento">Seguimiento</Link></li>
            </ul>
          </nav>
          <div className="user-menu">
            <InstallPWAButton />
            {user ? (
              <>
                <span>{user.nombre || ''} {user.apellidos || ''}</span>
                <button onClick={handleLogout} className="btn-logout">Cerrar Sesión</button>
              </>
            ) : (
              <button onClick={() => navigate('/login')} className="btn-login">Iniciar Sesión</button>
            )}
          </div>
        </div>
      </header>
      
      <main className="app-content">
        <div className="container">
          <Outlet />
        </div>
      </main>
      
      <footer className="app-footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} Paquetería Cuba - MVP</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;