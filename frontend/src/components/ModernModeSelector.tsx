import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Package,
  Star,
  Check,
  ArrowRight,
  Camera,
  QrCode,
  Zap,
  Shield
} from 'lucide-react';

// 🇨🇺 Selector de Modo Modernizado
const ModernModeSelector: React.FC = () => {
  const navigate = useNavigate();
  const [selectedMode, setSelectedMode] = useState<'simple' | 'premium' | null>(null);

  const modes = [
    {
      id: 'simple' as const,
      title: 'Modo Simple',
      subtitle: 'Para uso diario y rápido',
      description: 'Interfaz limpia y eficiente para crear envíos básicos sin complicaciones.',
      icon: Package,
      color: 'blue',
      gradient: 'from-blue-500 to-blue-600',
      features: [
        'Formulario simplificado',
        'Cálculo automático de precios',
        'Información esencial del envío',
        'Tracking básico',
        'Interfaz optimizada'
      ],
      route: '/envios/simple',
      recommended: false
    },
    {
      id: 'premium' as const,
      title: 'Modo Premium',
      subtitle: 'Funciones avanzadas completas',
      description: 'Herramientas profesionales con captura de fotos, códigos QR y análisis detallado.',
      icon: Star,
      color: 'amber',
      gradient: 'from-amber-500 to-amber-600',
      features: [
        'Captura de fotos optimizada',
        'Generación de códigos QR',
        'Conversión USD/CUP automática',
        'Etiquetas profesionales',
        'Análisis avanzado de envíos'
      ],
      route: '/envios/premium',
      recommended: true
    }
  ];

  const handleModeSelect = (mode: typeof modes[0]) => {
    setSelectedMode(mode.id);
    // Pequeña animación antes de navegar
    setTimeout(() => {
      navigate(mode.route);
    }, 300);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <Zap className="w-4 h-4" />
            <span>Selecciona tu modo de trabajo</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            ¿Cómo prefieres trabajar?
          </h1>

          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Elige el modo que mejor se adapte a tus necesidades.
            Puedes cambiar entre modos en cualquier momento.
          </p>
        </div>

        {/* Comparación de Modos */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {modes.map((mode) => {
            const IconComponent = mode.icon;
            const isSelected = selectedMode === mode.id;

            return (
              <div
                key={mode.id}
                className={`
                  relative bg-white rounded-2xl p-8 border-2 cursor-pointer transition-all duration-300 transform
                  ${isSelected
                    ? `border-${mode.color}-500 shadow-xl scale-105`
                    : 'border-gray-200 hover:border-gray-300 hover:shadow-lg hover:scale-102'
                  }
                `}
                onClick={() => handleModeSelect(mode)}
              >

                {/* Badge recomendado */}
                {mode.recommended && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <div className="bg-gradient-to-r from-amber-500 to-amber-600 text-white px-4 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                      <Shield className="w-3 h-3" />
                      <span>Recomendado</span>
                    </div>
                  </div>
                )}

                {/* Header del modo */}
                <div className="text-center mb-6">
                  <div className={`
                    inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-r ${mode.gradient} mb-4
                  `}>
                    <IconComponent className="w-8 h-8 text-white" />
                  </div>

                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    {mode.title}
                  </h3>

                  <p className={`text-${mode.color}-600 font-medium mb-3`}>
                    {mode.subtitle}
                  </p>

                  <p className="text-gray-600">
                    {mode.description}
                  </p>
                </div>

                {/* Lista de características */}
                <div className="space-y-3 mb-6">
                  {mode.features.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <div className={`w-5 h-5 rounded-full bg-${mode.color}-100 flex items-center justify-center`}>
                        <Check className={`w-3 h-3 text-${mode.color}-600`} />
                      </div>
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>

                {/* Botón de acción */}
                <button
                  className={`
                    w-full py-4 px-6 rounded-xl font-semibold transition-all duration-200 flex items-center justify-center space-x-2
                    ${isSelected
                      ? `bg-gradient-to-r ${mode.gradient} text-white shadow-lg`
                      : `bg-${mode.color}-50 text-${mode.color}-700 hover:bg-${mode.color}-100`
                    }
                  `}
                >
                  <span>{isSelected ? 'Accediendo...' : 'Seleccionar Modo'}</span>
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            );
          })}
        </div>

        {/* Características Especiales */}
        <div className="bg-white rounded-2xl p-8 border border-gray-200">
          <h3 className="text-xl font-bold text-gray-900 mb-6 text-center">
            Características Especiales del Modo Premium
          </h3>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center mx-auto mb-3">
                <Camera className="w-6 h-6 text-amber-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Captura de Fotos</h4>
              <p className="text-sm text-gray-600">
                Toma fotos directamente desde el navegador con compresión automática
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center mx-auto mb-3">
                <QrCode className="w-6 h-6 text-amber-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Códigos QR</h4>
              <p className="text-sm text-gray-600">
                Genera etiquetas con códigos QR para seguimiento profesional
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center mx-auto mb-3">
                <Shield className="w-6 h-6 text-amber-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Análisis Avanzado</h4>
              <p className="text-sm text-gray-600">
                Reportes detallados y métricas de rendimiento de envíos
              </p>
            </div>
          </div>
        </div>

        {/* Nota informativa */}
        <div className="text-center mt-8">
          <p className="text-gray-500 text-sm">
            💡 Puedes cambiar entre modos en cualquier momento desde el menú principal
          </p>
        </div>
      </div>
    </div>
  );
};

export default ModernModeSelector;
