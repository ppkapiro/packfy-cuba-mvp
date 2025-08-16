import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Plus, Search, List, User } from 'lucide-react';

// 📱 Navegación inferior móvil optimizada para PACKFY CUBA
const MobileBottomNav: React.FC = () => {
  const location = useLocation();

  const isActiveRoute = (path: string) => {
    if (path === '/dashboard') {
      return location.pathname === '/' || location.pathname === '/dashboard';
    }
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const navItems = [
    {
      path: '/dashboard',
      label: 'Inicio',
      icon: Home,
      isActive: isActiveRoute('/dashboard')
    },
    {
      path: '/envios',
      label: 'Gestión',
      icon: List,
      isActive: isActiveRoute('/envios') && !isActiveRoute('/envios/nuevo')
    },
    {
      path: '/envios/nuevo',
      label: 'Crear',
      icon: Plus,
      isActive: isActiveRoute('/envios/nuevo'),
      isHighlight: true // Botón principal destacado
    },
    {
      path: '/rastreo',
      label: 'Rastrear',
      icon: Search,
      isActive: isActiveRoute('/rastreo')
    },
    {
      path: '/perfil',
      label: 'Perfil',
      icon: User,
      isActive: isActiveRoute('/perfil') || isActiveRoute('/configuracion')
    }
  ];

  return (
    <nav className="mobile-bottom-nav">
      <div className="mobile-nav-items">
        {navItems.map((item) => {
          const IconComponent = item.icon;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`mobile-nav-item ${item.isActive ? 'active' : ''} ${item.isHighlight ? 'highlight' : ''}`}
            >
              <div className="mobile-nav-icon">
                <IconComponent size={20} />
              </div>
              <span className="mobile-nav-label">{item.label}</span>
              {item.isActive && <div className="mobile-nav-indicator" />}
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default MobileBottomNav;
