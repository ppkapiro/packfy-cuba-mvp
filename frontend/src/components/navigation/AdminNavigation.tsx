import { Link, useLocation } from 'react-router-dom';
import {
  BarChart3, Users, Settings, Package,
  TrendingUp, UserPlus, Cog, ExternalLink
} from 'lucide-react';
import '../../styles/admin-navigation.css';

interface AdminNavigationProps {
  isActiveRoute: (path: string) => boolean;
}

const AdminNavigation: React.FC<AdminNavigationProps> = ({ isActiveRoute }) => {
  return (
    <ul className="nav-menu admin-nav">
      {/* Dashboard Ejecutivo */}
      <li className="nav-item">
        <Link
          to="/admin/dashboard"
          className={`nav-link ${isActiveRoute('/admin/dashboard') ? 'active' : ''}`}
          title="Dashboard Ejecutivo"
        >
          <BarChart3 className="nav-icon" size={18} />
          <span>Dashboard</span>
        </Link>
      </li>

      {/* Gestión de Envíos */}
      <li className="nav-item dropdown">
        <Link
          to="/admin/envios"
          className={`nav-link ${isActiveRoute('/admin/envios') ? 'active' : ''}`}
          title="Gestión de Envíos"
        >
          <Package className="nav-icon" size={18} />
          <span>Envíos</span>
        </Link>
        <ul className="dropdown-menu">
          <li>
            <Link to="/admin/envios" className="dropdown-link">
              📋 Todos los Envíos
            </Link>
          </li>
          <li>
            <Link to="/admin/envios/nuevo" className="dropdown-link">
              ➕ Crear Envío
            </Link>
          </li>
          <li>
            <Link to="/admin/envios/estadisticas" className="dropdown-link">
              📊 Estadísticas
            </Link>
          </li>
        </ul>
      </li>

      {/* Gestión de Usuarios */}
      <li className="nav-item dropdown">
        <Link
          to="/admin/usuarios"
          className={`nav-link ${isActiveRoute('/admin/usuarios') ? 'active' : ''}`}
          title="Gestión de Usuarios"
        >
          <Users className="nav-icon" size={18} />
          <span>Usuarios</span>
        </Link>
        <ul className="dropdown-menu">
          <li>
            <Link to="/admin/usuarios" className="dropdown-link">
              👥 Ver Usuarios
            </Link>
          </li>
          <li>
            <Link to="/admin/usuarios/nuevo" className="dropdown-link">
              <UserPlus className="nav-icon-small" size={14} />
              Agregar Usuario
            </Link>
          </li>
          <li>
            <Link to="/admin/roles" className="dropdown-link">
              🔐 Roles y Permisos
            </Link>
          </li>
        </ul>
      </li>

      {/* Reportes y Analíticas */}
      <li className="nav-item">
        <Link
          to="/admin/reportes"
          className={`nav-link ${isActiveRoute('/admin/reportes') ? 'active' : ''}`}
          title="Reportes y Analíticas"
        >
          <TrendingUp className="nav-icon" size={18} />
          <span>Reportes</span>
        </Link>
      </li>

      {/* Configuración */}
      <li className="nav-item dropdown">
        <Link
          to="/admin/configuracion"
          className={`nav-link ${isActiveRoute('/admin/configuracion') ? 'active' : ''}`}
          title="Configuración"
        >
          <Settings className="nav-icon" size={18} />
          <span>Config</span>
        </Link>
        <ul className="dropdown-menu">
          <li>
            <Link to="/admin/empresa" className="dropdown-link">
              🏢 Datos de Empresa
            </Link>
          </li>
          <li>
            <Link to="/admin/configuracion/sistema" className="dropdown-link">
              <Cog className="nav-icon-small" size={14} />
              Sistema
            </Link>
          </li>
          <li>
            <a
              href="/admin/"
              target="_blank"
              rel="noopener noreferrer"
              className="dropdown-link"
            >
              <ExternalLink className="nav-icon-small" size={14} />
              Admin Django
            </a>
          </li>
        </ul>
      </li>
    </ul>
  );
};

export default AdminNavigation;
