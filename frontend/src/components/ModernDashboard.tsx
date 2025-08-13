import React from 'react';
import { Link } from 'react-router-dom';
import {
  Package,
  Search,
  BarChart3,
  Clock,
  TrendingUp,
  Star,
  Zap
} from 'lucide-react';

// 🇨🇺 Dashboard Modernizado con Mejor Distribución
const ModernDashboard: React.FC = () => {

  // Acciones rápidas principales
  const quickActions = [
    {
      title: 'Crear Envío Simple',
      description: 'Interfaz simplificada para envíos básicos',
      icon: Package,
      href: '/envios/simple',
      color: 'bg-blue-500',
      hoverColor: 'hover:bg-blue-600',
      textColor: 'text-blue-700',
      bgColor: 'bg-blue-50',
      iconColor: 'text-white'
    },
    {
      title: 'Crear Envío Premium',
      description: 'Funciones avanzadas con cámara y QR',
      icon: Star,
      href: '/envios/premium',
      color: 'bg-amber-500',
      hoverColor: 'hover:bg-amber-600',
      textColor: 'text-amber-700',
      bgColor: 'bg-amber-50',
      iconColor: 'text-white'
    },
    {
      title: 'Gestionar Envíos',
      description: 'Ver y administrar todos los envíos',
      icon: BarChart3,
      href: '/envios',
      color: 'bg-green-500',
      hoverColor: 'hover:bg-green-600',
      textColor: 'text-green-700',
      bgColor: 'bg-green-50',
      iconColor: 'text-white'
    },
    {
      title: 'Rastrear Envío',
      description: 'Seguimiento en tiempo real',
      icon: Search,
      href: '/rastreo',
      color: 'bg-purple-500',
      hoverColor: 'hover:bg-purple-600',
      textColor: 'text-purple-700',
      bgColor: 'bg-purple-50',
      iconColor: 'text-white'
    }
  ];

  // Estadísticas rápidas
  const stats = [
    {
      label: 'Envíos Hoy',
      value: '12',
      change: '+3',
      icon: Package,
      color: 'text-blue-600'
    },
    {
      label: 'En Tránsito',
      value: '8',
      change: '-1',
      icon: Clock,
      color: 'text-amber-600'
    },
    {
      label: 'Completados',
      value: '45',
      change: '+12',
      icon: TrendingUp,
      color: 'text-green-600'
    }
  ];

  return (
    <div className="space-y-8">

      {/* Header del Dashboard */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              ¡Bienvenido a Packfy Cuba! 🇨🇺
            </h1>
            <p className="text-blue-100 text-lg">
              Tu sistema de paquetería moderno y eficiente
            </p>
          </div>
          <div className="hidden md:block">
            <div className="w-24 h-24 bg-white/10 rounded-full flex items-center justify-center">
              <Package className="w-12 h-12 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Estadísticas Rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, index) => {
          const IconComponent = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="text-3xl font-bold text-gray-900">{stat.value}</span>
                    <span className={`text-sm font-medium ${
                      stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {stat.change}
                    </span>
                  </div>
                </div>
                <div className={`p-3 rounded-lg bg-gray-50`}>
                  <IconComponent className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Acciones Rápidas */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Acciones Rápidas</h2>
          <span className="text-sm text-gray-500">Selecciona una acción para comenzar</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => {
            const IconComponent = action.icon;
            return (
              <Link
                key={index}
                to={action.href}
                className="group bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-lg hover:border-gray-300 transition-all duration-200"
              >
                <div className="flex flex-col items-center text-center space-y-4">

                  {/* Icono */}
                  <div className={`
                    w-16 h-16 rounded-xl ${action.color} ${action.hoverColor}
                    flex items-center justify-center transition-colors group-hover:scale-105 transform duration-200
                  `}>
                    <IconComponent className={`w-8 h-8 ${action.iconColor}`} />
                  </div>

                  {/* Contenido */}
                  <div>
                    <h3 className="font-semibold text-gray-900 group-hover:text-gray-700 transition-colors">
                      {action.title}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {action.description}
                    </p>
                  </div>

                  {/* Indicador de acción */}
                  <div className={`
                    px-4 py-2 rounded-lg ${action.bgColor} ${action.textColor}
                    text-sm font-medium group-hover:scale-105 transform transition-all duration-200
                  `}>
                    Comenzar
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Sección de Ayuda Rápida */}
      <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-8">
        <div className="text-center">
          <Zap className="w-12 h-12 text-blue-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            ¿Necesitas ayuda?
          </h3>
          <p className="text-gray-600 mb-6">
            Accede a nuestras guías rápidas y tutoriales para sacar el máximo provecho del sistema
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-3 sm:space-y-0 sm:space-x-4">
            <Link
              to="/envios/modo"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Guía de Modos
            </Link>
            <Link
              to="/diagnostico"
              className="bg-white text-gray-700 px-6 py-3 rounded-lg font-medium border border-gray-300 hover:bg-gray-50 transition-colors"
            >
              Diagnóstico
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernDashboard;
