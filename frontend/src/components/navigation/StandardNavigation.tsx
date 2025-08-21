import { Link } from 'react-router-dom';
import { Package, Search, FileText, User } from 'lucide-react';

interface StandardNavigationProps {
  isActiveRoute: (path: string) => boolean;
}

const StandardNavigation: React.FC<StandardNavigationProps> = ({ isActiveRoute }) => {
  return (
    <ul className="nav-menu standard-nav">
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
          <Package className="nav-icon" size={18} />
          <span>Nuevo</span>
        </Link>
      </li>
      <li className="nav-item">
        <Link
          to="/envios"
          className={`nav-link ${isActiveRoute('/envios') && !isActiveRoute('/envios/nuevo') ? 'active' : ''}`}
        >
          <FileText className="nav-icon" size={18} />
          <span>Gestión</span>
        </Link>
      </li>
      <li className="nav-item">
        <Link
          to="/rastreo"
          className={`nav-link ${isActiveRoute('/rastreo') ? 'active' : ''}`}
          onClick={() => console.log('🔍 Layout: Navegando a /rastreo')}
        >
          <Search className="nav-icon" size={18} />
          <span>Rastrear</span>
        </Link>
      </li>
    </ul>
  );
};

export default StandardNavigation;
