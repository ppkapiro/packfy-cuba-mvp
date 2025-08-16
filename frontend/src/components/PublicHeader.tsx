import { Link } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';

const PublicHeader = () => {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className="public-header">
      <div className="public-header-content">
  <Link to="/" className="public-logo hover-lift">
          <span className="icon icon-flag-cuba icon-lg"></span>
          <span>Packfy Cuba</span>
        </Link>

        <nav className="public-nav">
          <Link to="/rastrear" className="public-nav-link hover-lift ripple pressable">
            <span className="icon icon-dashboard"></span>
            <span>🔍 Rastrear Paquete</span>
          </Link>
          <Link to="/login" className="public-nav-link hover-lift ripple pressable">
            <span className="icon icon-user"></span>
            <span>Iniciar Sesión</span>
          </Link>
          <button type="button" className="public-nav-link hover-lift ripple pressable" onClick={toggleTheme} aria-label="Cambiar tema">
            <span className="icon icon-sun"></span>
            <span>{theme === 'dark' ? 'Tema Claro' : 'Tema Oscuro'}</span>
          </button>
        </nav>
      </div>
    </header>
  );
};

export default PublicHeader;
