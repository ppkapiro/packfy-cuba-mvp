import React from 'react';
import { Outlet } from 'react-router-dom';
import Navigation from './Navigation';

// 🇨🇺 Layout Modernizado con Navegación Mejorada
const ModernLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navegación Mejorada */}
      <Navigation />

      {/* Contenido Principal */}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Outlet />
        </div>
      </main>

      {/* Footer opcional */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-4">
              <span>© 2024 Packfy Cuba</span>
              <span>•</span>
              <span>Sistema de Paquetería</span>
            </div>
            <div className="flex items-center space-x-4">
              <span>v3.0</span>
              <span>•</span>
              <span className="text-green-600 font-medium">En línea</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ModernLayout;
