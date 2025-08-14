import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, Star, ArrowRight } from 'lucide-react';

// 🇨🇺 Selector de Modo Simple para Crear Envíos
const ModeSelector: React.FC = () => {
  const navigate = useNavigate();

  const modes = [
    {
      id: 'simple',
      title: 'Modo Simple',
      subtitle: 'Gratis • Rápido • Fácil',
      description: 'Formulario básico para envíos estándar. Perfecto para uso diario.',
      icon: Package,
      color: 'blue',
      features: [
        'Formulario simplificado',
        'Campos esenciales únicamente',
        'Proceso rápido',
        'Interfaz limpia'
      ],
      route: '/envios/simple',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      textColor: 'text-blue-700'
    },
    {
      id: 'premium',
      title: 'Modo Premium',
      subtitle: 'Completo • Avanzado • Profesional',
      description: 'Formulario completo con todas las funciones avanzadas disponibles.',
      icon: Star,
      color: 'amber',
      features: [
        'Captura de fotos',
        'Códigos QR y etiquetas',
        'Conversión USD/CUP',
        'Análisis detallado'
      ],
      route: '/envios/premium',
      bgColor: 'bg-amber-50',
      borderColor: 'border-amber-200',
      textColor: 'text-amber-700'
    }
  ];

  const handleModeSelect = (route: string) => {
    navigate(route);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          📦 Crear Nuevo Envío
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Selecciona el modo que mejor se adapte a tus necesidades para crear el envío
        </p>
      </div>

      {/* Selector de Modos */}
      <div className="grid md:grid-cols-2 gap-6">
        {modes.map((mode) => {
          const IconComponent = mode.icon;
          return (
            <div
              key={mode.id}
              className={`
                relative p-6 rounded-xl border-2 cursor-pointer transition-all duration-200
                hover:shadow-lg hover:scale-105
                ${mode.bgColor} ${mode.borderColor}
              `}
              onClick={() => handleModeSelect(mode.route)}
            >
              {/* Icono y Título */}
              <div className="flex items-center mb-4">
                <div className={`
                  w-12 h-12 rounded-lg flex items-center justify-center mr-4
                  bg-white shadow-sm
                `}>
                  <IconComponent className={`w-6 h-6 ${mode.textColor}`} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">
                    {mode.title}
                  </h3>
                  <p className={`text-sm font-medium ${mode.textColor}`}>
                    {mode.subtitle}
                  </p>
                </div>
              </div>

              {/* Descripción */}
              <p className="text-gray-600 mb-4">
                {mode.description}
              </p>

              {/* Características */}
              <ul className="space-y-2 mb-6">
                {mode.features.map((feature, index) => (
                  <li key={index} className="flex items-center text-sm text-gray-700">
                    <div className={`
                      w-2 h-2 rounded-full mr-3
                      ${mode.id === 'simple' ? 'bg-blue-500' : 'bg-amber-500'}
                    `}></div>
                    {feature}
                  </li>
                ))}
              </ul>

              {/* Botón de Acción */}
              <button
                className={`
                  w-full flex items-center justify-center space-x-2
                  py-3 px-4 rounded-lg font-medium transition-all
                  ${mode.id === 'simple'
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-amber-600 hover:bg-amber-700 text-white'
                  }
                `}
                onClick={(e) => {
                  e.stopPropagation();
                  handleModeSelect(mode.route);
                }}
              >
                <span>Usar {mode.title}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          );
        })}
      </div>

      {/* Footer de Ayuda */}
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-500">
          ¿No estás seguro cuál elegir? El <strong>Modo Simple</strong> es perfecto para la mayoría de envíos.
          Puedes cambiar al <strong>Modo Premium</strong> en cualquier momento.
        </p>
      </div>
    </div>
  );
};

export default ModeSelector;
