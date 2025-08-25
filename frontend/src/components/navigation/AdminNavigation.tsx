import React from 'react';
import { Link } from 'react-router-dom';
import {
  BarChart3, Users, Settings, Package, TrendingUp
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
      <li className="nav-item">
        <Link
          to="/admin/envios"
          className={`nav-link ${isActiveRoute('/admin/envios') ? 'active' : ''}`}
          title="Gestión de Envíos"
        >
          <Package className="nav-icon" size={18} />
          <span>Envíos</span>
        </Link>
      </li>

      {/* Gestión de Usuarios */}
      <li className="nav-item">
        <Link
          to="/admin/usuarios"
          className={`nav-link ${isActiveRoute('/admin/usuarios') ? 'active' : ''}`}
          title="Gestión de Usuarios"
        >
          <Users className="nav-icon" size={18} />
          <span>Usuarios</span>
        </Link>
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
      <li className="nav-item">
        <Link
          to="/admin/configuracion"
          className={`nav-link ${isActiveRoute('/admin/configuracion') ? 'active' : ''}`}
          title="Configuración"
        >
          <Settings className="nav-icon" size={18} />
          <span>Config</span>
        </Link>
      </li>
    </ul>
  );
};

export default AdminNavigation;
