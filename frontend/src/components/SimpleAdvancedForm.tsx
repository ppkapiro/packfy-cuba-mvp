import React, { useState } from 'react';
import { Package, Camera, QrCode, DollarSign, Star } from 'lucide-react';

// Servicio de conversión simplificado
const SimpleCurrencyService = {
  rate: 320, // USD a CUP

  calculatePrice(weightLbs: number, hasInsurance = false): number {
    let basePrice = 8.50; // Precio base

    if (weightLbs > 2.2) basePrice = 15.00;  // >1kg
    if (weightLbs > 4.4) basePrice = 28.00;  // >2kg
    if (weightLbs > 11.0) basePrice = 45.00; // >5kg
    if (weightLbs > 22.0) basePrice = 85.00; // >10kg
    if (weightLbs > 44.0) basePrice = 85.00 + ((weightLbs - 44.0) * 2.04); // >20kg

    const insurance = hasInsurance ? basePrice * 0.05 : 0;
    const handling = basePrice * 0.15;

    return (basePrice + insurance + handling) * this.rate; // En CUP
  }
};

// Servicio de cámara simplificado
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

// Servicio de QR simplificado
const SimpleQRService = {
  generateTrackingNumber(): string {
    const timestamp = Date.now().toString().slice(-8);
    return `PCK${timestamp}`;
  },

  createQRData(packageInfo: any): string {
    return JSON.stringify({
      tracking: this.generateTrackingNumber(),
      weight: packageInfo.weight,
      destination: packageInfo.destination,
      created: new Date().toLocaleDateString()
    });
  }
};

// Componente Modo Simple (Gratuito)
const SimpleAdvancedForm: React.FC = () => {
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
    console.log('📷 Iniciando captura de foto...');
    try {
      const capturedPhoto = await SimpleCameraService.capturePhoto();
      console.log('📷 Resultado de captura:', capturedPhoto);

      if (capturedPhoto) {
        console.log('📷 Foto capturada exitosamente:', capturedPhoto.name, capturedPhoto.size);
        setPhoto(capturedPhoto);
        // No cambiar el step automáticamente, dejar que el usuario haga clic en "Continuar a QR"
      } else {
        console.log('📷 No se capturó ninguna foto (usuario canceló)');
      }
    } catch (error) {
      console.error('📷 Error capturando foto:', error);
      alert('Error capturando foto: ' + error);
    }
  };

  const handleGenerateQR = () => {
    const trackingNumber = SimpleQRService.generateTrackingNumber();
    setTracking(trackingNumber);
    alert(`¡Paquete registrado exitosamente!
Tracking: ${trackingNumber}
Precio: $${price?.toLocaleString()} CUP`);
  };

  const renderSteps = () => {
    const steps = [
      { key: 'info', label: 'Info', icon: Package, active: step === 'info' },
      { key: 'price', label: 'Precio', icon: DollarSign, active: step === 'price' },
      { key: 'photo', label: 'Foto', icon: Camera, active: step === 'photo' },
      { key: 'qr', label: 'QR', icon: QrCode, active: step === 'qr' }
    ];

    return (
      <div className="flex justify-center mb-6">
        {steps.map((s, i) => {
          const Icon = s.icon;
          return (
            <div key={s.key} className="flex items-center">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                s.active ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'
              }`}>
                <Icon className="w-5 h-5" />
              </div>
              <span className={`ml-2 text-sm ${s.active ? 'font-bold' : ''}`}>
                {s.label}
              </span>
              {i < steps.length - 1 && (
                <div className="w-8 h-px bg-gray-300 mx-4" />
              )}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-teal-50 py-8 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden">
          {/* Header con indicador de modo gratuito */}
          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-6 text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-full bg-white/10 backdrop-blur-sm"></div>
            <div className="relative z-10">
              <div className="inline-flex items-center bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm font-bold mb-3 border border-white/30">
                <Package className="w-4 h-4 mr-2" />
                MODO SIMPLE - GRATIS
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">
                🇨🇺 Packfy Cuba
              </h1>
              <p className="text-blue-100 text-lg">
                Registro de Paquete Simplificado
              </p>

              {/* Link a Premium mejorado */}
              <div className="mt-6 p-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl">
                <p className="text-white/90 text-sm mb-3">
                  ¿Necesitas funciones avanzadas?
                </p>
                <a
                  href="/envios"
                  className="inline-flex items-center bg-white text-blue-600 px-6 py-2 rounded-full font-bold text-sm hover:bg-blue-50 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  <Star className="w-4 h-4 mr-2" />
                  Actualizar a Premium ✨
                </a>
              </div>
            </div>
          </div>

          <div className="p-8">

        {renderSteps()}

        {step === 'info' && (
          <form onSubmit={handleInfoSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Remitente</label>
              <input
                type="text"
                value={formData.senderName}
                onChange={(e) => setFormData(prev => ({ ...prev, senderName: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="Tu nombre"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Destinatario</label>
              <input
                type="text"
                value={formData.recipientName}
                onChange={(e) => setFormData(prev => ({ ...prev, recipientName: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="Nombre del destinatario"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Dirección</label>
              <input
                type="text"
                value={formData.recipientAddress}
                onChange={(e) => setFormData(prev => ({ ...prev, recipientAddress: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="Dirección en Cuba"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Peso (libras)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                value={formData.weight}
                onChange={(e) => setFormData(prev => ({ ...prev, weight: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="2.5"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Descripción</label>
              <input
                type="text"
                value={formData.description}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="Contenido del paquete"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700"
            >
              Calcular Precio
            </button>
          </form>
        )}

        {step === 'price' && (
          <div className="text-center space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <h3 className="text-xl font-bold text-green-800 mb-2">
                Precio Calculado
              </h3>
              <div className="text-3xl font-bold text-green-600 mb-2">
                ${price?.toLocaleString()} CUP
              </div>
              <div className="text-sm text-green-700">
                Peso: {formData.weight} lbs • Tasa: 1 USD = 320 CUP
              </div>
            </div>

            <button
              onClick={() => setStep('photo')}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700"
            >
              Continuar a Foto
            </button>
          </div>
        )}

        {step === 'photo' && (
          <div className="text-center space-y-4">
            <h3 className="text-xl font-bold mb-4">Capturar Foto del Paquete</h3>

            {/* Debug info */}
            <div className="text-xs text-gray-500 mb-2">
              Debug: photo = {photo ? `${photo.name} (${photo.size} bytes)` : 'null'}
            </div>

            {photo && (
              <div className="mb-4">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  ✅ Foto capturada: {photo.name} ({(photo.size / 1024).toFixed(1)} KB)
                </div>
              </div>
            )}

            <button
              onClick={handleCapturePhoto}
              className="w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 flex items-center justify-center gap-2"
            >
              <Camera className="w-5 h-5" />
              {photo ? 'Cambiar Foto' : 'Capturar Foto'}
            </button>

            {photo && (
              <button
                onClick={() => {
                  console.log('🔄 Cambiando a step QR...');
                  setStep('qr');
                }}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700"
              >
                Continuar a QR
              </button>
            )}

            {/* Botón de debug para forzar continuar */}
            <button
              onClick={() => {
                console.log('🧪 Debug: Forzando paso a QR sin foto...');
                setStep('qr');
              }}
              className="w-full bg-yellow-500 text-white py-2 rounded-lg text-sm"
            >
              🧪 Debug: Continuar sin foto
            </button>
          </div>
        )}

        {step === 'qr' && (
          <div className="text-center space-y-4">
            <h3 className="text-xl font-bold mb-4">Generar Etiqueta QR</h3>

            <div className="bg-gray-50 border rounded-lg p-4 text-left text-sm">
              <div><strong>Remitente:</strong> {formData.senderName}</div>
              <div><strong>Destinatario:</strong> {formData.recipientName}</div>
              <div><strong>Dirección:</strong> {formData.recipientAddress}</div>
              <div><strong>Peso:</strong> {formData.weight} lbs</div>
              <div><strong>Precio:</strong> ${price?.toLocaleString()} CUP</div>
              {photo && <div><strong>Foto:</strong> ✅ Adjunta</div>}
            </div>

            {tracking && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="font-bold text-blue-800">Número de Tracking:</div>
                <div className="text-2xl font-mono text-blue-600">{tracking}</div>
              </div>
            )}

            <button
              onClick={handleGenerateQR}
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-medium hover:bg-purple-700 flex items-center justify-center gap-2"
            >
              <QrCode className="w-5 h-5" />
              Generar QR y Finalizar
            </button>
          </div>
        )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleAdvancedForm;
