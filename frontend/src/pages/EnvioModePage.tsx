import React, { useState } from 'react';
import { Package, Star, Lock, Check } from 'lucide-react';
import '../styles/envio-mode.css';
import '../styles/performance.css';
import '../styles/packfy-direct.css';

interface EnvioModePageProps {
  defaultMode?: 'simple' | 'premium';
}

const EnvioModePage: React.FC<EnvioModePageProps> = ({ defaultMode = 'simple' }) => {
  const [selectedMode, setSelectedMode] = useState<'simple' | 'premium'>(defaultMode);
  const [isPremiumUnlocked, setIsPremiumUnlocked] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);

  const features = {
    simple: [
      'Crear envíos básicos',
      'Cálculo simple de precios',
      'Información estándar de envío',
      'Tracking básico',
      'Interfaz simplificada',
      'Todas las funciones esenciales'
    ],
    premium: [
      'Crear envíos avanzados',
      'Cálculo avanzado de precios',
      'Captura de fotos optimizada',
      'QR codes y etiquetas profesionales',
      'Conversión USD/CUP automática',
      'Interfaz moderna responsive',
      'Soporte prioritario',
      'Análisis de envíos detallado'
    ]
  };

  const handlePremiumAccess = () => {
    if (!isPremiumUnlocked) {
      setShowPaymentModal(true);
    } else {
      setSelectedMode('premium');
      // Redirect to premium mode interface
      window.location.href = '/envios/premium';
    }
  };

  const handlePayment = () => {
    // Simular pago exitoso
    setIsPremiumUnlocked(true);
    setShowPaymentModal(false);
    setSelectedMode('premium');
    alert('¡Pago procesado! Ahora tienes acceso al modo Premium 🎉');
  };

  return (
    <div className="min-h-screen packfy-hero py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Partículas de fondo */}
        <div className="packfy-particles">
          <div className="packfy-particle"></div>
          <div className="packfy-particle"></div>
          <div className="packfy-particle"></div>
        </div>

        {/* Header mejorado con efectos avanzados */}
        <div className="text-center mb-16 slideUp">
          <div className="relative inline-flex items-center justify-center w-24 h-24 packfy-cuba-flag rounded-full mb-8 shadow-2xl">
            <span className="text-4xl">🇨🇺</span>
          </div>

          <h1 className="text-6xl font-bold packfy-title mb-6">
            Packfy Cuba
          </h1>

          <div className="max-w-3xl mx-auto">
            <p className="text-xl text-gray-600 leading-relaxed mb-4">
              � Gestiona todos tus envíos de forma eficiente y profesional
            </p>
            <p className="text-lg text-blue-600 font-medium">
              ✨ Comienza con gestión gratuita o desbloquea funciones premium por solo $5 USD
            </p>

            {/* Badges informativos */}
            <div className="flex flex-wrap justify-center items-center gap-4 mt-6">
              <span className="packfy-badge-cuba">
                <div className="w-2 h-2 bg-white rounded-full mr-2"></div>
                100% Cubano
              </span>
              <span className="packfy-badge-cuba">
                <div className="w-2 h-2 bg-white rounded-full mr-2"></div>
                Optimizado para móvil
              </span>
              <span className="packfy-badge-cuba">
                <div className="w-2 h-2 bg-white rounded-full mr-2"></div>
                Conversión USD/CUP
              </span>
            </div>
          </div>
        </div>

        {/* Mode Selection Cards con efectos mejorados */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12 relative z-10">
          {/* Modo Simple */}
          <div className={`packfy-card group relative bg-white rounded-3xl shadow-2xl p-8 border-2 ${
            selectedMode === 'simple' ? 'border-blue-500 ring-4 ring-blue-200 transform scale-105 packfy-glow' : 'border-gray-200 hover:border-blue-300'
          }`}>
            <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-t-3xl animate-shimmer"></div>

            {/* Efecto de brillo superior */}
            <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-gradient-to-r from-transparent via-blue-300 to-transparent blur-sm"></div>

            <div className="text-center mb-8">
              <div className="relative inline-flex items-center justify-center">
                <div className="absolute inset-0 bg-blue-100 rounded-full animate-pulse"></div>
                <div className="relative bg-gradient-to-r from-blue-500 to-cyan-500 w-20 h-20 rounded-full flex items-center justify-center mb-6 shadow-lg animate-breathe">
                  <Package className="w-10 h-10 text-white" />
                </div>
              </div>

              <div className="mb-4">
                <span className="inline-flex items-center bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-bold mb-3">
                  <Check className="w-4 h-4 mr-2" />
                  100% GRATIS
                </span>
              </div>

              <h2 className="text-3xl font-bold text-gray-800 mb-3">Modo Simple</h2>
              <p className="text-lg text-gray-600 leading-relaxed">
                Crea y gestiona envíos con funciones básicas. Perfecto para empezar sin costo.
              </p>
            </div>

            <ul className="space-y-4 mb-10">
              {features.simple.map((feature, index) => (
                <li key={index} className="flex items-center group-hover:translate-x-1 transition-transform duration-300">
                  <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                    <Check className="w-4 h-4 text-green-600" />
                  </div>
                  <span className="text-gray-700 font-medium">{feature}</span>
                </li>
              ))}
            </ul>

            <button
              onClick={() => {
                setSelectedMode('simple');
                window.location.href = '/envios/simple';
              }}
              className="packfy-btn-simple w-full py-4 px-8 rounded-2xl text-lg shadow-lg flex items-center justify-center gap-3"
            >
              <Package className="w-5 h-5" />
              Modo Simple
            </button>
          </div>

          {/* Modo Premium */}
          <div className={`packfy-card group relative bg-white rounded-3xl shadow-2xl p-8 border-2 ${
            selectedMode === 'premium' ? 'border-yellow-400 ring-4 ring-yellow-200 transform scale-105 packfy-glow' : 'border-gray-200 hover:border-yellow-300'
          }`}>
            {/* Premium Badge con efectos mejorados */}
            <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 z-10">
              <div className="packfy-premium-badge px-6 py-3 rounded-full text-sm flex items-center shadow-xl">
                <Star className="w-5 h-5 mr-2" />
                MÁS POPULAR
              </div>
            </div>

            <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 rounded-t-3xl animate-shimmer"></div>

            {/* Efecto de brillo superior premium */}
            <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-gradient-to-r from-transparent via-yellow-300 to-transparent blur-sm"></div>

            <div className="text-center mb-8 mt-6">
              <div className="relative inline-flex items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-100 to-orange-100 rounded-full animate-pulse"></div>
                <div className="relative bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 w-20 h-20 rounded-full flex items-center justify-center mb-6 shadow-lg animate-breathe">
                  <Star className="w-10 h-10 text-white animate-star-twinkle" />
                </div>
              </div>

              <div className="mb-4">
                <span className="inline-flex items-center bg-gradient-to-r from-yellow-100 to-orange-100 text-yellow-800 px-4 py-2 rounded-full text-sm font-bold mb-3 border border-yellow-300">
                  <Star className="w-4 h-4 mr-2" />
                  ACCESO COMPLETO
                </span>
              </div>

              <h2 className="text-3xl font-bold text-gray-800 mb-3">Modo Premium</h2>
              <div className="flex items-center justify-center gap-2 mb-3">
                <span className="text-4xl font-bold bg-gradient-to-r from-yellow-600 to-orange-600 bg-clip-text text-transparent">$5.00</span>
                <span className="text-lg text-gray-600 font-medium">USD</span>
              </div>
              <p className="text-lg text-gray-600 leading-relaxed">
                Funciones avanzadas y experiencia premium para crear envíos profesionales.
              </p>
            </div>

            <ul className="space-y-4 mb-10">
              {features.premium.map((feature, index) => (
                <li key={index} className="flex items-center group-hover:translate-x-1 transition-transform duration-300">
                  <div className="w-6 h-6 bg-gradient-to-r from-yellow-100 to-orange-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0 border border-yellow-300">
                    <Check className="w-4 h-4 text-yellow-600" />
                  </div>
                  <span className="text-gray-700 font-medium">{feature}</span>
                </li>
              ))}
            </ul>

            <button
              onClick={handlePremiumAccess}
              className={`w-full py-4 px-8 rounded-2xl text-lg shadow-lg flex items-center justify-center gap-3 ${
                isPremiumUnlocked
                  ? 'packfy-btn-simple'
                  : 'packfy-btn-premium'
              }`}
            >
              {isPremiumUnlocked ? (
                <>
                  <Check className="w-5 h-5" />
                  Acceder a Premium
                </>
              ) : (
                <>
                  <Lock className="w-5 h-5" />
                  Desbloquear Premium
                </>
              )}
            </button>
          </div>
        </div>

        {/* Comparación de funciones mejorada */}
        <div className="bg-white rounded-3xl shadow-xl p-8 mb-12 relative overflow-hidden">
          {/* Efecto de fondo sutil */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 via-transparent to-yellow-50/50"></div>

          <div className="relative z-10">
            <h3 className="text-4xl font-bold text-center text-gray-800 mb-4 animate-scale-in">
              ¿Por qué elegir Premium?
            </h3>
            <p className="text-center text-gray-600 mb-12 text-lg">
              Descubre todas las ventajas del modo premium
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg animate-breathe group-hover:animate-bounce-soft">
                  <span className="text-3xl">📱</span>
                </div>
                <h4 className="text-2xl font-bold text-gray-800 mb-4">Interfaz Moderna</h4>
                <p className="text-gray-600 leading-relaxed">
                  Diseño responsive optimizado para móviles cubanos con animaciones suaves y experiencia premium.
                </p>
              </div>

              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-r from-green-500 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg animate-breathe delay-half group-hover:animate-bounce-soft">
                  <span className="text-3xl">💰</span>
                </div>
                <h4 className="text-2xl font-bold text-gray-800 mb-4">Conversión USD/CUP</h4>
                <p className="text-gray-600 leading-relaxed">
                  Cálculos automáticos con la tasa actual del mercado cubano actualizada en tiempo real.
                </p>
              </div>

              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg animate-breathe delay-1 group-hover:animate-bounce-soft">
                  <span className="text-3xl">🚀</span>
                </div>
                <h4 className="text-2xl font-bold text-gray-800 mb-4">Funciones Avanzadas</h4>
                <p className="text-gray-600 leading-relaxed">
                  QR codes, categorización automática, cámara HD y herramientas profesionales completas.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Payment Modal mejorado */}
        {showPaymentModal && (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-lg flex items-center justify-center z-50 p-4 animate-fadeIn">
            {/* Efecto de partículas en el fondo */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <div className="absolute top-1/4 left-1/4 w-3 h-3 bg-yellow-400 rounded-full animate-star-twinkle"></div>
              <div className="absolute top-1/3 right-1/4 w-2 h-2 bg-blue-400 rounded-full animate-star-twinkle delay-1"></div>
              <div className="absolute bottom-1/3 left-1/3 w-2.5 h-2.5 bg-red-400 rounded-full animate-star-twinkle delay-2"></div>
            </div>

            <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl transform animate-scale-in relative overflow-hidden">
              {/* Efecto de brillo superior */}
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 animate-shimmer"></div>

              <div className="text-center mb-8">
                <div className="relative w-24 h-24 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl animate-breathe">
                  <div className="absolute -inset-2 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full blur opacity-30 animate-pulse"></div>
                  <Star className="w-12 h-12 text-white relative z-10 animate-star-twinkle" />
                </div>

                <h3 className="text-3xl font-bold text-gray-800 mb-3">
                  🚀 Desbloquear Premium
                </h3>
                <p className="text-gray-600 text-lg">
                  Accede a todas las funciones avanzadas
                </p>

                <div className="mt-6 p-6 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-2xl border-2 border-yellow-200 shadow-inner">
                  <div className="text-4xl font-bold text-yellow-600 animate-pulse">$5.00 USD</div>
                  <div className="text-sm text-gray-600 mt-2 font-medium">
                    ✨ Pago único • 🔓 Acceso de por vida • 🇨🇺 Optimizado para Cuba
                  </div>
                </div>
              </div>

              <div className="space-y-4 mb-8">
                <button
                  onClick={handlePayment}
                  className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white py-4 px-6 rounded-2xl font-bold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 flex items-center justify-center gap-3 animate-scale-in"
                >
                  <span className="text-2xl animate-bounce-soft">💳</span>
                  <span>Pagar con PayPal</span>
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                </button>

                <button
                  onClick={handlePayment}
                  className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-4 px-6 rounded-2xl font-bold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 flex items-center justify-center gap-3 animate-scale-in delay-half"
                >
                  <span className="text-2xl animate-bounce-soft">💰</span>
                  <span>Pagar con Transfermóvil</span>
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                </button>
              </div>

              <button
                onClick={() => setShowPaymentModal(false)}
                className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 px-6 rounded-2xl font-medium transition-all duration-200 hover:transform hover:scale-105"
              >
                ❌ Cancelar
              </button>
            </div>
          </div>
        )}

        {/* Footer mejorado con estadísticas */}
        <div className="text-center mt-16">
          <div className="bg-white rounded-3xl shadow-lg p-8 mb-8 relative overflow-hidden">
            {/* Efecto de fondo sutil */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-50/30 via-transparent to-red-50/30"></div>

            <div className="relative z-10">
              {/* Estadísticas impresionantes */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 animate-pulse">99.9%</div>
                  <div className="text-sm text-gray-600 font-medium">Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 animate-pulse delay-half">24/7</div>
                  <div className="text-sm text-gray-600 font-medium">Soporte</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 animate-pulse delay-1">100%</div>
                  <div className="text-sm text-gray-600 font-medium">Cubano</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600 animate-pulse delay-2">$5</div>
                  <div className="text-sm text-gray-600 font-medium">Premium</div>
                </div>
              </div>

              <div className="flex flex-wrap justify-center items-center gap-8 mb-6">
                <div className="flex items-center gap-3 text-gray-600 group">
                  <div className="w-4 h-4 bg-green-500 rounded-full animate-pulse group-hover:animate-bounce-soft"></div>
                  <span className="font-medium">🔒 100% Seguro</span>
                </div>
                <div className="flex items-center gap-3 text-gray-600 group">
                  <div className="w-4 h-4 bg-blue-500 rounded-full animate-pulse delay-half group-hover:animate-bounce-soft"></div>
                  <span className="font-medium">🌐 Soporte 24/7</span>
                </div>
                <div className="flex items-center gap-3 text-gray-600 group">
                  <div className="w-4 h-4 bg-yellow-500 rounded-full animate-pulse delay-1 group-hover:animate-bounce-soft"></div>
                  <span className="font-medium">🇨🇺 Optimizado para Cuba</span>
                </div>
              </div>

              <div className="border-t border-gray-200 pt-6">
                <p className="text-gray-500 text-lg font-medium mb-2">
                  🚀 Packfy Cuba - La Revolución de la Paquetería
                </p>
                <p className="text-gray-400 text-sm">
                  Diseñado especialmente para el mercado cubano • Versión 2.0 • Con amor desde Cuba 🇨🇺
                </p>

                {/* Versión y fecha */}
                <div className="mt-4 text-xs text-gray-400 space-y-1">
                  <div>✨ Última actualización: Agosto 2025</div>
                  <div>🔧 Build: v2.0.0-premium</div>
                  <div>💻 Optimizado para móviles cubanos</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnvioModePage;
