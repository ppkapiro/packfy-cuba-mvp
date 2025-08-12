import React, { useState } from 'react';
import { Package, Camera, QrCode, DollarSign, Check, ArrowRight, ArrowLeft, Star } from 'lucide-react';
import '../styles/envio-mode.css';

// Servicios simplificados (misma lógica)
const SimpleCurrencyService = {
  rate: 320,
  calculatePrice(weightLbs: number, hasInsurance = false): number {
    let basePrice = 8.50;
    if (weightLbs > 2.2) basePrice = 15.00;  // >1kg
    if (weightLbs > 4.4) basePrice = 28.00;  // >2kg
    if (weightLbs > 11.0) basePrice = 45.00; // >5kg
    if (weightLbs > 22.0) basePrice = 85.00; // >10kg
    if (weightLbs > 44.0) basePrice = 85.00 + ((weightLbs - 44.0) * 2.04); // >20kg

    const insurance = hasInsurance ? basePrice * 0.05 : 0;
    const handling = basePrice * 0.15;
    return (basePrice + insurance + handling) * this.rate;
  },
  getWeightCategory(weightLbs: number): string {
    if (weightLbs <= 2.2) return 'Paquete Pequeño (0-2.2 lbs)';
    if (weightLbs <= 4.4) return 'Paquete Mediano (2.2-4.4 lbs)';
    if (weightLbs <= 11.0) return 'Paquete Grande (4.4-11 lbs)';
    if (weightLbs <= 22.0) return 'Paquete Extra Grande (11-22 lbs)';
    if (weightLbs <= 44.0) return 'Paquete Jumbo (22-44 lbs)';
    return 'Paquete Comercial (44+ lbs)';
  }
};

const SimpleCameraService = {
  async capturePhoto(): Promise<File | null> {
    return new Promise((resolve) => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.capture = 'environment';

      input.onchange = (e) => {
        const file = (e.target as HTMLInputElement).files?.[0];
        resolve(file || null);
      };

      input.oncancel = () => resolve(null);
      input.click();
    });
  }
};

const SimpleQRService = {
  generateTrackingNumber(): string {
    const timestamp = Date.now().toString().slice(-8);
    return `PCK${timestamp}`;
  }
};

const ModernAdvancedForm: React.FC = () => {
  const [step, setStep] = useState<'info' | 'price' | 'photo' | 'qr'>('info');
  const [formData, setFormData] = useState({
    senderName: '',
    recipientName: '',
    recipientAddress: '',
    weight: '',
    description: ''
  });
  const [price, setPrice] = useState<number | null>(null);
  const [photo, setPhoto] = useState<File | null>(null);
  const [tracking, setTracking] = useState<string>('');

  const handleInfoSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.senderName && formData.recipientName && formData.weight) {
      const calculatedPrice = SimpleCurrencyService.calculatePrice(parseFloat(formData.weight));
      setPrice(calculatedPrice);
      setStep('price');
    }
  };

  const handleCapturePhoto = async () => {
    try {
      const capturedPhoto = await SimpleCameraService.capturePhoto();
      if (capturedPhoto) {
        setPhoto(capturedPhoto);
      }
    } catch (error) {
      alert('Error capturando foto: ' + error);
    }
  };

  const handleGenerateQR = () => {
    const trackingNumber = SimpleQRService.generateTrackingNumber();
    setTracking(trackingNumber);
    alert(`¡Paquete registrado exitosamente!\n\nTracking: ${trackingNumber}\nPrecio: $${price?.toLocaleString()} CUP`);
  };

  const steps = [
    { key: 'info', label: 'Información', icon: Package },
    { key: 'price', label: 'Precio', icon: DollarSign },
    { key: 'photo', label: 'Fotos', icon: Camera },
    { key: 'qr', label: 'Finalizar', icon: QrCode }
  ];

  const currentStepIndex = steps.findIndex(s => s.key === step);

  const renderStepIndicator = () => (
    <div className="flex justify-between items-center mb-6 sm:mb-8 px-2 sm:px-4">
      {steps.map((s, index) => {
        const Icon = s.icon;
        const isActive = step === s.key;
        const isCompleted = index < currentStepIndex;

        return (
          <div key={s.key} className="flex flex-col items-center flex-1 relative">
            <div className={`
              w-12 h-12 sm:w-16 sm:h-16 md:w-20 md:h-20 rounded-full flex items-center justify-center mb-2 transition-all duration-300 transform
              ${isActive ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white scale-110 shadow-xl ring-4 ring-blue-200' :
                isCompleted ? 'bg-gradient-to-br from-green-500 to-green-600 text-white shadow-lg' :
                'bg-gray-200 text-gray-400 hover:bg-gray-300'}
            `}>
              {isCompleted ? (
                <Check className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10" />
              ) : (
                <Icon className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10" />
              )}
            </div>
            <span className={`text-xs sm:text-sm md:text-base font-medium text-center px-1 transition-colors ${
              isActive ? 'text-blue-600 font-bold' :
              isCompleted ? 'text-green-600 font-semibold' : 'text-gray-400'
            }`}>
              {s.label}
            </span>
            {index < steps.length - 1 && (
              <div
                className={`absolute top-6 sm:top-8 md:top-10 left-1/2 h-0.5 sm:h-1 -z-10 transition-colors transform translate-x-6 sm:translate-x-8 md:translate-x-10 ${
                  isCompleted ? 'bg-gradient-to-r from-green-400 to-green-500' : 'bg-gray-300'
                } w-full`}
              />
            )}
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 fadeIn">
      {/* Header Premium con animaciones avanzadas */}
      <div className="gradient-premium shadow-2xl relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -skew-x-12 shimmer"></div>
        <div className="max-w-md mx-auto px-4 sm:px-6 py-6 sm:py-8 relative z-10">
          <div className="text-center slideUp">
            <div className="inline-flex items-center bg-white/30 backdrop-blur-lg text-white px-4 py-2 rounded-full text-xs sm:text-sm font-bold mb-3 border border-white/40 glow shadow-lg">
              <Star className="w-4 h-4 sm:w-5 sm:h-5 mr-2 float" />
              MODO PREMIUM ACTIVADO
              <div className="w-2 h-2 bg-green-400 rounded-full ml-2 animate-pulse"></div>
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-white mb-2 tracking-tight">
              🇨🇺 Packfy Cuba Premium
            </h1>
            <p className="text-yellow-100 text-sm sm:text-base opacity-90">
              Paquetería Profesional con Tecnología Avanzada
            </p>
            <div className="flex justify-center items-center mt-3 space-x-4 text-white/80 text-xs">
              <span className="flex items-center">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-1"></div>
                Cámara HD
              </span>
              <span className="flex items-center">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-1"></div>
                QR Tracking
              </span>
              <span className="flex items-center">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-1"></div>
                Sin límites
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Contenido principal con animaciones */}
      <div className="max-w-sm sm:max-w-md lg:max-w-lg xl:max-w-xl 2xl:max-w-2xl mx-auto px-3 sm:px-4 py-4 sm:py-6">
        {renderStepIndicator()}

        <div className="card-hover bg-white rounded-3xl shadow-2xl overflow-hidden backdrop-blur-sm bg-opacity-95 slideUp">
          {/* Paso 1: Información Premium */}
          {step === 'info' && (
            <div className="p-6 sm:p-8">
              <div className="text-center mb-6 sm:mb-8 fadeIn">
                <div className="gradient-premium w-16 h-16 sm:w-20 sm:h-20 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg glow">
                  <Package className="w-8 h-8 sm:w-10 sm:h-10 text-white float" />
                </div>
                <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-2">Información del Paquete Premium</h2>
                <p className="text-gray-600 text-sm sm:text-base">Sistema avanzado con todas las funcionalidades</p>
                <div className="inline-flex items-center bg-gradient-to-r from-green-100 to-blue-100 text-green-700 px-3 py-1 rounded-full text-xs font-medium mt-2">
                  ✨ Funciones Premium Desbloqueadas
                </div>
              </div>

              <form onSubmit={handleInfoSubmit} className="space-y-4 sm:space-y-6">
                <div className="space-y-4">
                  <div className="group">
                    <label className="block text-base sm:text-lg font-medium text-gray-700 mb-2 sm:mb-3 group-focus-within:text-blue-600 transition-colors">
                      👤 Remitente
                    </label>
                    <input
                      type="text"
                      value={formData.senderName}
                      onChange={(e) => setFormData(prev => ({ ...prev, senderName: e.target.value }))}
                      className="w-full px-4 sm:px-6 py-3 sm:py-4 text-base sm:text-lg border-2 border-gray-200 rounded-xl sm:rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-200 focus:outline-none transition-all duration-200 hover:border-gray-300"
                      placeholder="Tu nombre completo"
                      required
                    />
                  </div>

                  <div className="group">
                    <label className="block text-base sm:text-lg font-medium text-gray-700 mb-2 sm:mb-3 group-focus-within:text-blue-600 transition-colors">
                      🏠 Destinatario
                    </label>
                    <input
                      type="text"
                      value={formData.recipientName}
                      onChange={(e) => setFormData(prev => ({ ...prev, recipientName: e.target.value }))}
                      className="w-full px-4 sm:px-6 py-3 sm:py-4 text-base sm:text-lg border-2 border-gray-200 rounded-xl sm:rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-200 focus:outline-none transition-all duration-200 hover:border-gray-300"
                      placeholder="Nombre del destinatario"
                      required
                    />
                  </div>

                  <div className="group">
                    <label className="block text-base sm:text-lg font-medium text-gray-700 mb-2 sm:mb-3 group-focus-within:text-blue-600 transition-colors">
                      📍 Dirección en Cuba
                    </label>
                    <textarea
                      value={formData.recipientAddress}
                      onChange={(e) => setFormData(prev => ({ ...prev, recipientAddress: e.target.value }))}
                      className="w-full px-4 sm:px-6 py-3 sm:py-4 text-base sm:text-lg border-2 border-gray-200 rounded-xl sm:rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-200 focus:outline-none transition-all duration-200 hover:border-gray-300 h-20 sm:h-24 resize-none"
                      placeholder="Calle, número, municipio, provincia"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="group">
                      <label className="block text-base sm:text-lg font-medium text-gray-700 mb-2 sm:mb-3 group-focus-within:text-blue-600 transition-colors">
                        ⚖️ Peso (kg)
                      </label>
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        value={formData.weight}
                        onChange={(e) => setFormData(prev => ({ ...prev, weight: e.target.value }))}
                        className="w-full px-4 sm:px-6 py-3 sm:py-4 text-base sm:text-lg border-2 border-gray-200 rounded-xl sm:rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-200 focus:outline-none transition-all duration-200 hover:border-gray-300"
                        placeholder="2.5"
                        required
                      />
                    </div>

                    <div className="group">
                      <label className="block text-base sm:text-lg font-medium text-gray-700 mb-2 sm:mb-3 group-focus-within:text-blue-600 transition-colors">
                        📦 Tipo
                      </label>
                      <select
                        className="w-full px-4 sm:px-6 py-3 sm:py-4 text-base sm:text-lg border-2 border-gray-200 rounded-xl sm:rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-200 focus:outline-none transition-all duration-200 hover:border-gray-300 bg-white"
                        title="Tipo de paquete"
                        aria-label="Seleccionar tipo de paquete"
                      >
                        <option>Ropa</option>
                        <option>Zapatos</option>
                        <option>Electrónicos</option>
                        <option>Medicinas</option>
                        <option>Otros</option>
                      </select>
                    </div>
                  </div>

                  <div className="group">
                    <label className="block text-base sm:text-lg font-medium text-gray-700 mb-2 sm:mb-3 group-focus-within:text-blue-600 transition-colors">
                      📝 Descripción (opcional)
                    </label>
                    <input
                      type="text"
                      value={formData.description}
                      onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                      className="w-full px-4 sm:px-6 py-3 sm:py-4 text-base sm:text-lg border-2 border-gray-200 rounded-xl sm:rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-200 focus:outline-none transition-all duration-200 hover:border-gray-300"
                      placeholder="Detalles adicionales"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white py-3 sm:py-4 px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-3 focus:ring-4 focus:ring-blue-200"
                >
                  <span>Calcular Precio</span>
                  <ArrowRight className="w-5 h-5 sm:w-6 sm:h-6" />
                </button>
              </form>
            </div>
          )}

          {/* Paso 2: Precio */}
          {step === 'price' && (
            <div className="p-6 sm:p-8 text-center">
              <div className="bg-gradient-to-br from-green-500 to-emerald-600 w-16 h-16 sm:w-20 sm:h-20 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-lg">
                <DollarSign className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
              </div>
              <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800 mb-4 sm:mb-6">Precio Calculado</h2>

              <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl sm:rounded-3xl p-6 sm:p-8 mb-6 sm:mb-8 shadow-lg">
                <div className="text-3xl sm:text-4xl lg:text-5xl font-bold text-green-600 mb-2 sm:mb-3">
                  ${price?.toLocaleString()} CUP
                </div>
                <div className="text-base sm:text-lg lg:text-xl text-green-700 mb-3 sm:mb-4">
                  Peso: {formData.weight} kg
                </div>
                <div className="text-sm sm:text-base text-green-600 font-medium">
                  Tasa: 1 USD = 320 CUP
                </div>

                {/* Información adicional */}
                <div className="mt-4 sm:mt-6 pt-4 border-t border-green-200">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 text-sm sm:text-base">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Precio USD:</span>
                      <span className="font-semibold">${(price! / 320).toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Categoría:</span>
                      <span className="font-semibold">{SimpleCurrencyService.getWeightCategory(parseFloat(formData.weight))}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                <button
                  onClick={() => setStep('info')}
                  className="flex-1 bg-gray-200 text-gray-700 py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg hover:bg-gray-300 transition-all duration-200 flex items-center justify-center gap-2 transform hover:scale-105 active:scale-95"
                >
                  <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5" />
                  Atrás
                </button>
                <button
                  onClick={() => setStep('photo')}
                  className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 focus:ring-4 focus:ring-blue-200"
                >
                  Continuar
                  <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5" />
                </button>
              </div>
            </div>
          )}

          {/* Paso 3: Fotos */}
          {step === 'photo' && (
            <div className="p-6 sm:p-8 text-center">
              <div className="bg-gradient-to-br from-purple-500 to-indigo-600 w-16 h-16 sm:w-20 sm:h-20 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-lg">
                <Camera className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
              </div>
              <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800 mb-4 sm:mb-6">Fotos del Paquete</h2>
              <p className="text-sm sm:text-base text-gray-600 mb-6 sm:mb-8">Captura una foto clara del paquete</p>

              {photo && (
                <div className="bg-green-50 border-2 border-green-200 rounded-xl sm:rounded-2xl p-4 sm:p-6 mb-6 sm:mb-8 shadow-lg">
                  <div className="text-green-600 font-bold text-lg sm:text-xl mb-2">
                    ✅ Foto Capturada
                  </div>
                  <div className="text-green-700 text-sm sm:text-base">
                    {photo.name} ({(photo.size / 1024).toFixed(1)} KB)
                  </div>
                  <div className="mt-3 sm:mt-4">
                    <div className="w-full h-32 sm:h-40 bg-green-100 rounded-lg border-2 border-dashed border-green-300 flex items-center justify-center">
                      <span className="text-green-600 font-medium text-sm sm:text-base">Imagen guardada ✓</span>
                    </div>
                  </div>
                </div>
              )}

              <button
                onClick={handleCapturePhoto}
                className="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-4 sm:py-6 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-3 mb-6 sm:mb-8 focus:ring-4 focus:ring-purple-200"
              >
                <Camera className="w-6 h-6 sm:w-8 sm:h-8" />
                {photo ? 'Cambiar Foto' : 'Capturar Foto'}
              </button>

              <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                <button
                  onClick={() => setStep('price')}
                  className="flex-1 bg-gray-200 text-gray-700 py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg hover:bg-gray-300 transition-all duration-200 flex items-center justify-center gap-2 transform hover:scale-105 active:scale-95"
                >
                  <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5" />
                  Atrás
                </button>
                <button
                  onClick={() => setStep('qr')}
                  className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 focus:ring-4 focus:ring-blue-200"
                >
                  Continuar
                  <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5" />
                </button>
              </div>
            </div>
          )}

          {/* Paso 4: QR */}
          {step === 'qr' && (
            <div className="p-6 sm:p-8 text-center">
              <div className="bg-gradient-to-br from-indigo-500 to-purple-600 w-16 h-16 sm:w-20 sm:h-20 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-lg">
                <QrCode className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
              </div>
              <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800 mb-4 sm:mb-6">Finalizar Registro</h2>
              <p className="text-sm sm:text-base text-gray-600 mb-6 sm:mb-8">Revisa los datos y finaliza tu envío</p>

              <div className="bg-gray-50 rounded-xl sm:rounded-2xl p-4 sm:p-6 text-left mb-6 sm:mb-8 shadow-lg">
                <h3 className="font-bold text-lg sm:text-xl mb-4 text-center text-gray-800">📋 Resumen del Paquete</h3>
                <div className="space-y-3 sm:space-y-4 text-sm sm:text-base lg:text-lg">
                  <div className="flex justify-between items-center pb-2 border-b border-gray-200">
                    <span className="text-gray-600"><strong>👤 De:</strong></span>
                    <span className="font-medium text-right flex-1 ml-3">{formData.senderName}</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-gray-200">
                    <span className="text-gray-600"><strong>🏠 Para:</strong></span>
                    <span className="font-medium text-right flex-1 ml-3">{formData.recipientName}</span>
                  </div>
                  <div className="flex justify-between items-start pb-2 border-b border-gray-200">
                    <span className="text-gray-600"><strong>📍 Dirección:</strong></span>
                    <span className="font-medium text-right flex-1 ml-3 break-words">{formData.recipientAddress}</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-gray-200">
                    <span className="text-gray-600"><strong>⚖️ Peso:</strong></span>
                    <span className="font-medium">{formData.weight} kg</span>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-gray-200">
                    <span className="text-gray-600"><strong>💰 Precio:</strong></span>
                    <span className="font-bold text-green-600 text-lg sm:text-xl">${price?.toLocaleString()} CUP</span>
                  </div>
                  {photo && (
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600"><strong>📷 Foto:</strong></span>
                      <span className="font-medium text-green-600">✅ Adjunta</span>
                    </div>
                  )}
                </div>
              </div>

              {tracking && (
                <div className="bg-blue-50 border-2 border-blue-200 rounded-xl sm:rounded-2xl p-4 sm:p-6 mb-6 sm:mb-8 shadow-lg">
                  <div className="font-bold text-blue-800 text-lg sm:text-xl mb-3">🏷️ Número de Tracking:</div>
                  <div className="text-2xl sm:text-3xl lg:text-4xl font-mono text-blue-600 font-bold break-all">{tracking}</div>
                  <div className="mt-3 text-xs sm:text-sm text-blue-600">Guarda este número para seguir tu envío</div>
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                <button
                  onClick={() => setStep('photo')}
                  className="flex-1 bg-gray-200 text-gray-700 py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg hover:bg-gray-300 transition-all duration-200 flex items-center justify-center gap-2 transform hover:scale-105 active:scale-95"
                >
                  <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5" />
                  Atrás
                </button>
                <button
                  onClick={handleGenerateQR}
                  className="flex-1 bg-gradient-to-r from-indigo-500 to-indigo-600 text-white py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 focus:ring-4 focus:ring-indigo-200"
                >
                  <QrCode className="w-5 h-5 sm:w-6 sm:h-6" />
                  Finalizar
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer responsivo */}
      <div className="text-center py-4 sm:py-6 text-gray-500">
        <p className="text-xs sm:text-sm">🇨🇺 Packfy Cuba - Paquetería Moderna</p>
        <p className="text-xs text-gray-400 mt-1">Diseñado para móviles cubanos</p>
      </div>
    </div>
  );
};

export default ModernAdvancedForm;
