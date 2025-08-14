import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  Package,
  Plus,
  Search,
  Settings,
  Menu,
  X,
  Home,
  List,
  Star
} from 'lucide-react';

// 🇨🇺 Componente de Navegación Mejorado
const Navigation: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Verificar si la ruta está activa
  const isActiveRoute = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  // Elementos de navegación principales
  const mainNavItems = [
    {
      path: '/dashboard',
      label: 'Inicio',
      icon: Home,
      description: 'Panel principal',
      isActive: isActiveRoute('/dashboard')
    },
    {
      path: '/envios/nuevo',
      label: 'Crear',
      icon: Plus,
      description: 'Nuevo envío',
      isActive: isActiveRoute('/envios/nuevo')
    },
    {
      path: '/envios',
      label: 'Gestión',
      icon: List,
      description: 'Administrar envíos',
      isActive: isActiveRoute('/envios') && !isActiveRoute('/envios/nuevo')
    },
    {
      path: '/rastreo',
      label: 'Rastrear',
      icon: Search,
      description: 'Seguimiento',
      isActive: isActiveRoute('/rastreo')
    }
  ];

  // Elementos de navegación secundaria
  const quickActions = [
    {
      path: '/envios/simple',
      label: 'Modo Simple',
      icon: Package,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      path: '/envios/premium',
      label: 'Modo Premium',
      icon: Star,
      color: 'text-amber-600',
      bgColor: 'bg-amber-50'
    }
  ];

  return (
    <>
      {/* Header Principal */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">

            {/* Logo */}
            <Link
              to="/dashboard"
              className="flex items-center space-x-3 text-xl font-bold text-gray-900 hover:text-blue-600 transition-colors"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                <Package className="w-5 h-5 text-white" />
              </div>
              <span className="hidden sm:block">Packfy Cuba</span>
            </Link>

            {/* Navegación Desktop */}
            <nav className="hidden md:flex items-center space-x-1">
              {mainNavItems.map((item) => {
                const IconComponent = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`
                      flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
                      ${item.isActive
                        ? 'bg-blue-100 text-blue-700 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                      }
                    `}
                    title={item.description}
                  >
                    <IconComponent className="w-4 h-4" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>

            {/* Menú de Usuario */}
            <div className="flex items-center space-x-4">

              {/* Acciones Rápidas - Desktop */}
              <div className="hidden lg:flex items-center space-x-2">
                {quickActions.map((action) => {
                  const IconComponent = action.icon;
                  return (
                    <Link
                      key={action.path}
                      to={action.path}
                      className={`
                        flex items-center space-x-1 px-3 py-1.5 rounded-md text-xs font-medium transition-all
                        ${action.bgColor} ${action.color} hover:shadow-sm
                      `}
                      title={action.label}
                    >
                      <IconComponent className="w-3 h-3" />
                      <span className="hidden xl:block">{action.label}</span>
                    </Link>
                  );
                })}
              </div>

              {/* Info del Usuario */}
              {user && (
                <div className="hidden sm:flex items-center space-x-3">
                  <div className="text-right">
                    <div className="text-sm font-medium text-gray-900">
                      {user.nombre || user.email?.split('@')[0]}
                    </div>
                    <div className="text-xs text-gray-500">
                      {user.email}
                    </div>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="text-gray-400 hover:text-gray-600 transition-colors"
                    title="Cerrar sesión"
                    aria-label="Cerrar sesión"
                  >
                    <Settings className="w-5 h-5" />
                  </button>
                </div>
              )}

              {/* Botón Menú Móvil */}
              <button
                className="md:hidden p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                title="Abrir menú"
                aria-label="Abrir menú de navegación"
              >
                {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Menú Móvil */}
      {isMenuOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-white">
          <div className="flex flex-col h-full">

            {/* Header del menú móvil */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                  <Package className="w-5 h-5 text-white" />
                </div>
                <span className="text-lg font-bold text-gray-900">Packfy Cuba</span>
              </div>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                title="Cerrar menú"
                aria-label="Cerrar menú"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Navegación móvil */}
            <nav className="flex-1 p-4">
              <div className="space-y-2">
                {mainNavItems.map((item) => {
                  const IconComponent = item.icon;
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setIsMenuOpen(false)}
                      className={`
                        flex items-center space-x-3 px-4 py-3 rounded-lg transition-all
                        ${item.isActive
                          ? 'bg-blue-100 text-blue-700'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                        }
                      `}
                    >
                      <IconComponent className="w-5 h-5" />
                      <div>
                        <div className="font-medium">{item.label}</div>
                        <div className="text-sm text-gray-500">{item.description}</div>
                      </div>
                    </Link>
                  );
                })}
              </div>

              {/* Acciones rápidas móvil */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-900 mb-3">Acciones Rápidas</h3>
                <div className="space-y-2">
                  {quickActions.map((action) => {
                    const IconComponent = action.icon;
                    return (
                      <Link
                        key={action.path}
                        to={action.path}
                        onClick={() => setIsMenuOpen(false)}
                        className={`
                          flex items-center space-x-3 px-4 py-3 rounded-lg transition-all
                          ${action.bgColor} ${action.color}
                        `}
                      >
                        <IconComponent className="w-5 h-5" />
                        <span className="font-medium">{action.label}</span>
                      </Link>
                    );
                  })}
                </div>
              </div>
            </nav>

            {/* Usuario en móvil */}
            {user && (
              <div className="p-4 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">
                      {user.nombre || user.email?.split('@')[0]}
                    </div>
                    <div className="text-sm text-gray-500">{user.email}</div>
                  </div>
                  <button
                    onClick={() => {
                      handleLogout();
                      setIsMenuOpen(false);
                    }}
                    className="flex items-center space-x-2 px-3 py-2 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
                  >
                    <Settings className="w-4 h-4" />
                    <span className="text-sm font-medium">Salir</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default Navigation;
