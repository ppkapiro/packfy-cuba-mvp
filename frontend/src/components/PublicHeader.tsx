import { Link } from 'react-router-dom';

const PublicHeader = () => {
  return (
    <header className="public-header">
      <div className="public-header-content">
        <Link to="/" className="public-logo">
          <span className="icon icon-flag-cuba icon-lg"></span>
          <span>Packfy Cuba</span>
        </Link>

        <nav className="public-nav">
          <Link to="/rastrear" className="public-nav-link">
            <span className="icon icon-dashboard"></span>
            <span>🔍 Rastrear Paquete</span>
          </Link>
          <Link to="/login" className="public-nav-link">
            <span className="icon icon-user"></span>
            <span>Iniciar Sesión</span>
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default PublicHeader;
